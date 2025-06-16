import io
import IPython.display
import numpy as np
import PIL.Image
import os
input_folder = "test_images/old"
output_folder = "output"
basepath = os.getcwd()
input_path = os.path.join(basepath, input_folder)
output_path = os.path.join(basepath, output_folder)
os.mkdir(output_path)


def imshow(a, format='png', jpeg_fallback=True):
    a = np.asarray(a, dtype=np.uint8)
    data = io.BytesIO()
    PIL.Image.fromarray(a).save(data, format)
    im_data = data.getvalue()
    try:
        disp = IPython.display.display(IPython.display.Image(im_data))
    except IOError:
        if jpeg_fallback and format != 'jpeg':
            print(('Warning: image was too large to display in format "{}"; '
                   'trying jpeg instead.').format(format))
            return imshow(a, format='jpeg')
        else:
            raise
    return disp


def make_grid(I1, I2, resize=True):
    I1 = np.asarray(I1)
    H, W = I1.shape[0], I1.shape[1]

    if I1.ndim >= 3:
        I2 = np.asarray(I2.resize((W, H)))
        I_combine = np.zeros((H, W * 2, 3))
        I_combine[:, :W, :] = I1[:, :, :3]
        I_combine[:, W:, :] = I2[:, :, :3]
    else:
        I2 = np.asarray(I2.resize((W, H)).convert('L'))
        I_combine = np.zeros((H, W * 2))
        I_combine[:, :W] = I1[:, :]
        I_combine[:, W:] = I2[:, :]
    I_combine = PIL.Image.fromarray(np.uint8(I_combine))

    W_base = 600
    if resize:
        ratio = W_base / (W * 2)
        H_new = int(H * ratio)
        I_combine = I_combine.resize((W_base, H_new), PIL.Image.LANCZOS)

    return I_combine

filenames = os.listdir(os.path.join(input_path))
filenames.sort()

for filename in filenames:
    print(filename)
    image_original = PIL.Image.open(os.path.join(input_path, filename))
    image_restore = PIL.Image.open(os.path.join(output_path, 'final_output', filename))

    display(make_grid(image_original, image_restore))