import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import cv2 as cv
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors

img = cv.imread('speed sign test 1.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

pixel_colors = img.reshape((np.shape(img)[0]*np.shape(img)[1], 3))
norm = colors.Normalize(vmin=-1.,vmax=1.)
norm.autoscale(pixel_colors)
pixel_colors = norm(pixel_colors).tolist()

hsv_img = cv.cvtColor(img, cv.COLOR_RGB2HSV)
h, s, v = cv.split(hsv_img)
fig = plt.figure()
axis = fig.add_subplot(1, 1, 1, projection="3d")

axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
axis.set_xlabel("Hue")
axis.set_ylabel("Saturation")
axis.set_zlabel("Value")
#plt.show()

light_red = (1,150,100)
dark_red = (24,255,255)
mask = cv.inRange(hsv_img, light_red, dark_red)
result = cv.bitwise_and(img, img, mask=mask)

other_red = (165,150,50)
other_darker_red = (255,255,250)
mask_other = cv.inRange(hsv_img, other_red, other_darker_red)
result_other = cv.bitwise_and(img, img, mask=mask)

final_mask = mask + mask_other
final_result = cv.bitwise_and(img, img, mask=final_mask)

# Taking a matrix of size 5 as the kernel
kernel = np.ones((3, 3), np.uint8)
kernel_close = np.ones((5,5), np.uint8)

# The first parameter is the original image,
# kernel is the matrix with which image is
# convolved and third parameter is the number
# of iterations, which will determine how much
# you want to erode/dilate a given image.
img_erosion = cv.erode(final_mask, kernel, iterations=1)
img_dilation = cv.dilate(final_mask, kernel, iterations=1)
img_de = cv.erode(img_dilation, kernel, iterations=1)
img_ded = cv.dilate(img_de, kernel, iterations=2)
closing = cv.morphologyEx(img_ded, cv.MORPH_CLOSE, kernel_close)
img_dedce = cv.erode(closing, kernel, iterations=2)

cv.imshow('Input', final_mask)
#cv.imshow('Erosion', img_erosion)
#cv.imshow('Dilation', img_dilation)
cv.imshow('Dilation then Erosion', img_de)
#cv.imshow('Dil, Er, Del', img_ded)
cv.imshow('Closing', img_dedce)

cv.waitKey(0)
