import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import cv2 as cv
from matplotlib import colors

img = cv.imread('sign.jpg')
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
dark_red = (23,255,255)
mask = cv.inRange(hsv_img, light_red, dark_red)
result = cv.bitwise_and(img, img, mask=mask)

other_red = (165,85,85)
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
detected_circles = cv.HoughCircles(gray_blurred,cv.HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=10,maxRadius=80)

# circle_points = len(detected_circles[0, :])
circle_loc = []

# Draw circles that are detected.
if detected_circles is not None:
    print(detected_circles[0, :])

    # Convert the circle parameters a, b and r to integers.
    detected_circles = np.uint16(np.around(detected_circles))
    iPoint = 0

    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]
        margin = 1  # extra margin so that ROI is a little larger than the circle
        r = r+margin
        circle_loc.append([a, b, r])
        iPoint = iPoint + 1

        roiSquare = r**2

        roi = final_result[b-r:b+r, a-r:a+r]
        roi = cv.cvtColor(roi, cv.COLOR_BGR2RGB)

        cv.imshow("ROI test", roi)
        cv.waitKey(0)
        roi.save('roi_example.jpg')

if detected_circles is None:
    print('no signs detected')

#for loc in circle_loc:
#    a, b, r = loc[0], loc[1], loc[2]
#    roi = final_mask[b-r:b+r, a-r:a+r]
#    cv.imshow("ROI test", roi)
#    cv.waitKey(0)
