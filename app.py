# sudoku solver
#
import cv2
from wraper.sudoku_wrapper import wrap
from ml_detector.sudoku_digitextract import *
from libraries import sudokusolver

print("""
############################################################################
                        sudoku solver
############################################################################""")
path = "sudoku3.png"
sudoku_img = cv2.imread(path)
img = wrap(path)
cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
sudoku = clean_image(sudoku_img)
sudoku_matrix, sudoku_clean = predict_digits(sudoku)
print(sudoku_matrix)
sudoku_matrix = sudokusolver.solve_sudoku(sudoku_matrix)
print(sudoku_matrix)
