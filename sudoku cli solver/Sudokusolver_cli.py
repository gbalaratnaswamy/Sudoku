from libraries import sudokusolver
import numpy as np
sudoku = np.zeros((9,9),dtype=np.int)
print("""
############################################################################
                        sudoku solver
############################################################################""")
print("enter values")
for i in range(9) :
    str_input = input().split(",")
    for j in range(9):
        sudoku[i,j]=str_input[j]

print(sudoku)
print("solution")
print(sudokusolver.solve_sudoku(sudoku))