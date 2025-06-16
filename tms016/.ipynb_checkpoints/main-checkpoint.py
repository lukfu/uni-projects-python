import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
from matplotlib import colors

img = cv.imread('sign7.png')
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

light_red = (0,100,50)
dark_red = (23,255,255) # H to 23~25 for yellow
mask = cv.inRange(hsv_img, light_red, dark_red)
result = cv.bitwise_and(img, img, mask=mask)

other_red = (165,100,50)
other_darker_red = (255,255,250)
mask_other = cv.inRange(hsv_img, other_red, other_darker_red)
result_other = cv.bitwise_and(img, img, mask=mask)

final_mask = mask + mask_other
final_result = cv.bitwise_and(img, img, mask=final_mask)

#plt.subplot(1,3,1)
#plt.imshow(final_mask, cmap="gray")
plt.subplot(1,2,1)
plt.imshow(final_result)
plt.subplot(1,2,2)
plt.imshow(img)
plt.show()
