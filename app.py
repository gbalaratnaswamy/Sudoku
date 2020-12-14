# sudoku solver
#
from wraper.sudoku_wrapper import wrap
from ml_detector.sudoku_digitextract import *
from libraries import sudokusolver

print("""
############################################################################
                        sudoku solver
############################################################################""")
path = "sudoku3.png"
wrap_image = wrap(path)
sudoku = clean_image(wrap_image)
sudoku_matrix, sudoku_clean = predict_digits(sudoku)
sudoku_matrix = sudokusolver.solve_sudoku(sudoku_matrix)
print(sudoku_matrix)
