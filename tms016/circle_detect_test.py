import numpy as np
from PIL import Image
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

light_red = (0,100,50)
dark_red = (15,255,255) # H to 23~25 for yellow
mask = cv.inRange(hsv_img, light_red, dark_red)
result = cv.bitwise_and(img, img, mask=mask)

other_red = (165,100,50)
other_darker_red = (255,255,250)
mask_other = cv.inRange(hsv_img, other_red, other_darker_red)
result_other = cv.bitwise_and(img, img, mask=mask)

final_mask = mask + mask_other
final_result = cv.bitwise_and(img, img, mask=final_mask)

# Convert to grayscale.
gray = cv.cvtColor(final_result, cv.COLOR_BGR2GRAY)

# Blur using 3 * 3 kernel.
gray_blurred = cv.blur(gray, (3, 3))

# Apply Hough transform on the blurred image.
detected_circles = cv.HoughCircles(gray_blurred,cv.HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=1,maxRadius=80)

# Draw circles that are detected.
if detected_circles is not None:

    # Convert the circle parameters a, b and r to integers.
    detected_circles = np.uint16(np.around(detected_circles))

    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]

        # Draw the circumference of the circle.
        cv.circle(final_result, (a, b), r, (0, 255, 0), 2)

        # Draw a small circle (of radius 1) to show the center.
        cv.circle(final_result, (a, b), 1, (0, 0, 255), 3)
        cv.imshow("Detected Circle", cv.cvtColor(final_result, cv.COLOR_BGR2RGB))
        cv.waitKey(0)

if detected_circles is None:
    print('no circles detected')
