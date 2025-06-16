try:
    # if on Windows, use the provided setup script to add the DLLs folder to the PATH
    from windows_setup import configure_path  # imports configure_path method from windows_setup.py

    configure_path()
except ImportError:
    configure_path = None

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

try:
    #  For python 2.7 tkinter is named Tkinter
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import typing
import threading

try:
    #  For Python 2.7 queue is named Queue
    import Queue as queue
except ImportError:
    import queue
from PIL import Image, ImageTk

from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, OPERATION_MODE, TLCamera, Frame
from thorlabs_tsi_sdk.tl_mono_to_color_processor import MonoToColorProcessorSDK
from thorlabs_tsi_sdk.tl_camera_enums import SENSOR_TYPE
from thorlabs_tsi_sdk.tl_mono_to_color_enums import COLOR_SPACE
from thorlabs_tsi_sdk.tl_color_enums import FORMAT

"""
Getting image data: when TLCamera instance is armed and triggered, poll for frame from the camera.
The image buffer can be directly used, e.g for colour processing. Image buffer is temporary and may
be invalidate after another image poll, rearming the camera or closing the camera.

TLCamera.dispose() and TLCameraSDK.dispose() cleans up camera resources. 

image_poll_timeout_ms: if the SDK could not get an image within the timeout, none will be returned.
"""


def show_image(image_input_array):
    cv.imshow('test', image_input_array)
    cv.waitKey(0)


def show_image_sequence(image_input, num_frames):
    for j in range(num_frames):
        plt.imshow(image_input[:, :, j])
        plt.title('frame' + str(j))
        plt.pause(5)


class LiveViewCanvas(tk.Canvas):

    def __init__(self, parent, image_queue):
        # type: (typing.Any, queue.Queue) -> LiveViewCanvas
        self.image_queue = image_queue
        self._image_width = 0
        self._image_height = 0
        tk.Canvas.__init__(self, parent)
        self.pack()
        self._get_image()

    def _get_image(self):
        try:
            image = self.image_queue.get_nowait()
            self._image = ImageTk.PhotoImage(master=self, image=image)
            if (self._image.width() != self._image_width) or (self._image.height() != self._image_height):
                # resize the canvas to match the new image size
                self._image_width = self._image.width()
                self._image_height = self._image.height()
                self.config(width=self._image_width, height=self._image_height)
            self.create_image(0, 0, image=self._image, anchor='nw')
        except queue.Empty:
            pass
        self.after(10, self._get_image)


""" ImageAcquisitionThread

This class derives from threading.Thread and is given a TLCamera instance during initialization. When started, the 
thread continuously acquires frames from the camera and converts them to PIL Image objects. These are placed in a 
queue.Queue object that can be retrieved using get_output_queue(). The thread doesn't do any arming or triggering, 
so users will still need to setup and control the camera from a different thread. Be sure to call stop() when it is 
time for the thread to stop.

"""


class ImageAcquisitionThread(threading.Thread):

    def __init__(self, camera):
        # type: (TLCamera) -> ImageAcquisitionThread
        super(ImageAcquisitionThread, self).__init__()
        self._camera = camera
        self._previous_timestamp = 0

        # setup color processing if necessary
        if self._camera.camera_sensor_type != SENSOR_TYPE.BAYER:
            # Sensor type is not compatible with the color processing library
            self._is_color = False
        else:
            self._mono_to_color_sdk = MonoToColorProcessorSDK()
            self._image_width = self._camera.image_width_pixels
            self._image_height = self._camera.image_height_pixels
            self._mono_to_color_processor = self._mono_to_color_sdk.create_mono_to_color_processor(
                SENSOR_TYPE.BAYER,
                self._camera.color_filter_array_phase,
                self._camera.get_color_correction_matrix(),
                self._camera.get_default_white_balance_matrix(),
                self._camera.bit_depth
            )
            self._is_color = True

        self._bit_depth = camera.bit_depth
        self._camera.image_poll_timeout_ms = 0  # Do not want to block for long periods of time
        self._image_queue = queue.Queue(maxsize=2)
        self._stop_event = threading.Event()

    def get_output_queue(self):
        # type: (type(None)) -> queue.Queue
        return self._image_queue

    def stop(self):
        self._stop_event.set()

    def _get_color_image(self, frame):
        # type: (Frame) -> Image
        # verify the image size
        width = frame.image_buffer.shape[1]
        height = frame.image_buffer.shape[0]
        if (width != self._image_width) or (height != self._image_height):
            self._image_width = width
            self._image_height = height
            print("Image dimension change detected, image acquisition thread was updated")
        # color the image. transform_to_24 will scale to 8 bits per channel
        color_image_data = self._mono_to_color_processor.transform_to_24(frame.image_buffer,
                                                                         self._image_width,
                                                                         self._image_height)
        color_image_data = color_image_data.reshape(self._image_height, self._image_width, 3)
        # return PIL Image object
        return Image.fromarray(color_image_data, mode='RGB')

    def _get_image(self, frame):
        # type: (Frame) -> Image
        # no coloring, just scale down image to 8 bpp and place into PIL Image object
        scaled_image = frame.image_buffer >> (self._bit_depth - 8)
        return Image.fromarray(scaled_image)

    def run(self):
        while not self._stop_event.is_set():
            try:
                frame = self._camera.get_pending_frame_or_null()
                if frame is not None:
                    if self._is_color:
                        pil_image = self._get_color_image(frame)
                    else:
                        pil_image = self._get_image(frame)
                    self._image_queue.put_nowait(pil_image)
            except queue.Full:
                # No point in keeping this image around when the queue is full, let's skip to the next one
                pass
            except Exception as error:
                print("Encountered error: {error}, image acquisition will stop.".format(error=error))
                break
        print("Image acquisition has stopped")
        if self._is_color:
            self._mono_to_color_processor.dispose()
            self._mono_to_color_sdk.dispose()


with TLCameraSDK() as sdk:
    camera_list = sdk.discover_available_cameras()
    print("Starting live view for camera focus adjusting")
    input("Press Enter to begin live view...")
    with sdk.open_camera(camera_list[0]) as camera:
        # create generic Tk App with just a LiveViewCanvas widget
        print("Generating app...")
        root = tk.Tk()
        root.title(camera.name)
        image_acquisition_thread = ImageAcquisitionThread(camera)
        camera_widget = LiveViewCanvas(parent=root, image_queue=image_acquisition_thread.get_output_queue())

        print("Setting camera parameters...")
        camera.frames_per_trigger_zero_for_unlimited = 0
        camera.arm(2)
        camera.issue_software_trigger()

        print("Starting image acquisition thread...")
        image_acquisition_thread.start()

        print("App starting")
        root.mainloop()

        print("Waiting for image acquisition thread to finish...")
        image_acquisition_thread.stop()
        image_acquisition_thread.join()

        print("Closing resources...")
        input("Press Enter to continue to image polling...")

NUM_FRAMES = 3
FRAMES_PER_SECOND = 100  # exposure_time_us = 1/FRAMES_PER_SECOND * 10^6
with TLCameraSDK() as sdk, MonoToColorProcessorSDK() as mono_to_color_sdk:
    available_cameras = sdk.discover_available_cameras()
    # print(available_cameras)
    if len(available_cameras) < 1:
        print("no cameras available")

    with sdk.open_camera(available_cameras[0]) as camera:  # opens sdk.available_camera as variable camera
        """
        General Camera Settings
        """
        camera.exposure_time_us = 1000  # set exposure in microseconds (/1000 for milliseconds)
        camera.frames_per_trigger_zero_for_unlimited = 0  # start camera in continuous mode if 0
        camera.image_poll_timeout_ms = 2000  # 1000 = 1 second polling timeout
        old_roi = camera.roi  # store the current roi (default roi)
        # camera.roi = (100, 100, 200, 200)  # set roi to be at origin point (100, 100) with a width & height of 100

        if camera.gain_range.max > 0:
            db_gain = 0
            gain_index = camera.convert_decibels_to_gain(db_gain)
            camera.gain = gain_index
            print(f"Set camera gain to {camera.convert_gain_to_decibels(camera.gain)}")

        camera.arm(2)  # arms the camera, argument is frames_to_buffer, why 2?

        image_width = camera.image_width_pixels
        image_height = camera.image_height_pixels

        camera.issue_software_trigger()  # software trigger, starts acquisition

        frame = camera.get_pending_frame_or_null()
        if frame is not None:
            print("frame received")
            # print(frame.image_buffer)
        else:
            raise ValueError("no frame arrived within the timeout")

        saved_frames = np.zeros((image_height, image_width, NUM_FRAMES), dtype=np.int16)
        for i in range(NUM_FRAMES):
            frame = camera.get_pending_frame_or_null()  # drop the for loop and you get just one frame
            if frame is not None:
                print("frame #{} received!".format(frame.frame_count))

                # print(frame.image_buffer)  # .../ perform operations using the data from image_buffer

                #  NOTE: frame.image_buffer is a temporary memory buffer that may be overwritten during the next call
                #        to get_pending_frame_or_null. The following line makes a deep copy of the image data:
                image_buffer_copy = np.copy(frame.image_buffer)
                saved_frames[:, :, i] = image_buffer_copy
            else:
                print("timeout reached during polling, program exiting...")
                break

        camera.disarm()  # disarm camera, disarming doesnt wipe the frame buffer
        camera.roi = old_roi  # reset ROI

print("program finished")
# saved_frames = [height, width, frame number in order]
saved_frames = saved_frames / 4
#show_image_sequence(saved_frames, NUM_FRAMES)

"""
Generate a Tk App using the LiveViewCanvas widget to display the saved frames.

Later add a way to export the saved frames as a video of given FPS replay.
Also find out how the FPS of the image polling can be examined.
"""
image = saved_frames[:,:,0]
show_image(image)
# show_image_sequence(saved_frames, FRAMES_PER_SECOND)
# im = Image.fromarray(saved_frames)
# im.show()
