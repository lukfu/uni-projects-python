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


NUM_FRAMES = 1
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
print(image.shape)
im = Image.fromarray(saved_frames)
im.show()
