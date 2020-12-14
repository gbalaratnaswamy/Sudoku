from matplotlib import pyplot as plt
from cv2 import cv2
from cv2 import cv2 as cv
import numpy as np


def wrap(path):
    img = cv2.imread(path)

    # resizing the image can give any value  for now i'm commenting them
    # img = imutils.resize(img, width=340)
    # img = imutils.resize(img, height=440)

    # finding the contours
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(imgray, 3)
    th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    contours, hierarchy = cv2.findContours(th3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # printing the number of contours
    print("Number of contours = " + str(len(contours)))

    # checking for the max area contour
    ctr_max_area = 0
    ctr_max = 0
    for ctr in contours:
        if cv2.contourArea(ctr) > ctr_max_area:
            ctr_max_area = cv2.contourArea(ctr)
            ctr_max = ctr

    # drawing the contours on the img
    cv2.drawContours(img, [ctr_max], 0, (0, 255, 0), 3)

    # unwrapping our ctr_max contour
    b = np.array([ctr_max[:, 0]])

    # defining some variables
    sum_max = 0
    diff_max = 0
    arr = []

    # finding all the corners according to the logic

    # for bottom-right
    for i in range(len(b[0])):
        x, y = b[0][i]
        if x + y > sum_max:
            sum_max = x + y
            arr.append(i)
    br_x, br_y = b[0][arr[-1]]

    # for top-left
    for i in range(len(b[0])):
        x, y = b[0][i]
        if x + y < sum_max:
            sum_max = x + y
            arr.append(i)
    tl_x, tl_y = b[0][arr[-1]]

    # for top-right
    for i in range(len(b[0])):
        x, y = b[0][i]
        if x - y > diff_max:
            diff_max = x - y
            arr.append(i)
    tr_x, tr_y = b[0][arr[-1]]

    # for bottom-left
    for i in range(len(b[0])):
        x, y = b[0][i]
        if x - y < diff_max:
            diff_max = x - y
            arr.append(i)
    bl_x, bl_y = b[0][arr[-1]]

    # marking the corner points of the contour in our img
    cv2.circle(img, (br_x, br_y), 5, (0, 0, 255), -1)
    cv2.circle(img, (bl_x, bl_y), 5, (0, 0, 255), -1)
    cv2.circle(img, (tr_x, tr_y), 5, (0, 0, 255), -1)
    cv2.circle(img, (tl_x, tl_y), 5, (0, 0, 255), -1)

    # calculating the size of the sudoku in original image
    height_new = max(bl_y - tl_y, br_y - tr_y)
    width_new = max(tr_x - tl_x, br_x - bl_x)

    # for perspective wrapping of the the desired part of image
    pts1 = np.float32([[tl_x, tl_y], [tr_x, tr_y], [bl_x, bl_y], [br_x, br_y]])
    pts2 = np.float32([[0, 0], [width_new, 0], [0, height_new], [width_new, height_new]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, M, (width_new, height_new))

    # thresholding our wrapped image
    imgray1 = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    blur1 = cv2.medianBlur(imgray1, 3)
    th4 = cv2.adaptiveThreshold(blur1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # showing all the images
    # cv2.imshow('Image', img)
    # cv2.imshow("th3", th3)
    # cv2.imshow("cropped", dst)
    # cv2.imshow("th4", th4)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return dst
