import tensorflow as tf
import numpy as np
import cv2


# define function to calculate max value of xy
def maxxy(contour):
    max_val = 0
    maxvxy = 0
    for pt in contour:
        temp_val = pt[0][0] * pt[0][1]
        if temp_val > max_val:
            max_val = temp_val
        if ((56 - pt[0][0]) * (56 - pt[0][1])) > maxvxy:
            maxvxy = (56 - pt[0][0]) * (56 - pt[0][1])
    return max_val, maxvxy


# load saved model trained for digit identification
def clean_image(sudoku):
    # image make up
    sudoku = cv2.cvtColor(sudoku, cv2.COLOR_BGR2GRAY)
    sudoku = cv2.GaussianBlur(sudoku, (5, 5), 0)
    sudoku = cv2.adaptiveThreshold(sudoku, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    sudoku = cv2.bitwise_not(sudoku, sudoku)
    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
    sudoku = cv2.erode(sudoku, kernel, iterations=1)
    sudoku = cv2.dilate(sudoku, kernel)
    sudoku = cv2.resize(sudoku, (504, 504))
    return sudoku


def predict_digits(sudoku):
    # load model pre trained
    new_model = tf.keras.models.load_model('ml_detector/saved_model/new_model')
    digit_predict = tf.keras.Sequential([new_model, tf.keras.layers.Softmax()])
    sudoku_matrix = np.zeros((9, 9), dtype=int)
    sudoku_clean = np.zeros((252, 252))
    for i in range(9):
        for j in range(9):
            # extract digit form sudoku
            digit_img = sudoku[i * 56:(i + 1) * 56, j * 56:(j + 1) * 56]
            # distinguish digit and noise, borders
            contours, her = cv2.findContours(digit_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            index = 0
            try:
                while cv2.contourArea(contours[index]) > 1000:
                    index = index + 1
            except IndexError:
                sudoku_matrix[i, j] = 0
                continue
            try:
                xy, x_y = maxxy(contours[index])
                while not (500 < x_y < 2500 and 900 < xy < 2500):
                    index = index + 1
                    xy, x_y = maxxy(contours[index])
            except IndexError:
                sudoku_matrix[i, j] = 0

                continue
            temp_contour = cv2.drawContours(np.zeros((56, 56), dtype=np.uint8), contours, index, 255, -1)
            try:
                moment = cv2.moments(contours[index])
                cx = int(moment['m10'] / moment['m00'])
                cy = int(moment['m01'] / moment['m00'])
            except ZeroDivisionError:
                sudoku_matrix[i, j] = 0
                continue
            # extra check layer if it was digit
            if 7 < cx < 50 and 7 < cy < 50 and cv2.contourArea(contours[index]) > 100:
                # transform digit to center
                wrap_matrix = np.float32([[1, 0, 28 - cx], [0, 1, 28 - cy]])
                digit_img = cv2.warpAffine(digit_img, wrap_matrix, (56, 56))
                temp_contour = cv2.warpAffine(temp_contour, wrap_matrix, (56, 56))
                digit = cv2.resize(cv2.bitwise_and(digit_img, temp_contour), (28, 28)) / 255
                sudoku_clean[i * 28:(i + 1) * 28, j * 28:(j + 1) * 28] = digit
                temp_contour = digit.reshape(1, 28, 28, 1)
                guess = digit_predict.predict(temp_contour)
                value = np.argmax(guess)
                if value == 0:
                    # value may be 8 or 9
                    sudoku_matrix[i, j] = np.argmax(guess[0, 1:]) + 1
                else:
                    sudoku_matrix[i, j] = value
            else:
                # no digit
                sudoku_matrix[i, j] = 0
    return sudoku_matrix, sudoku_clean
