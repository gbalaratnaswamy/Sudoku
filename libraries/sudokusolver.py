def generate_num():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]


def solve_sudoku(sudoku):
    count = 0
    sudoku_solve = sudoku.copy()
    value = {}
    while count < 81:
        if sudoku[count // 9][count % 9] != 0:
            count = count + 1
            continue
        if str(count) in value:
            pass
        else:
            value[str(count)] = generate_num()
        for i in range(9):
            temp = sudoku[count // 9][i]
            if temp != 0:
                if temp in value[str(count)]:
                    value[str(count)].remove(temp)
            else:
                if (count // 9) * 9 + i < count:
                    temp = sudoku_solve[count // 9][i]
                    if temp in value[str(count)]:
                        value[str(count)].remove(temp)
            temp = sudoku[i][count % 9]
            if temp != 0:
                if temp in value[str(count)]:
                    value[str(count)].remove(temp)
            else:
                if i * 9 + (count % 9) < count:
                    temp = sudoku_solve[i][count % 9]
                    if temp in value[str(count)]:
                        value[str(count)].remove(temp)
        if len(value[str(count)]) == 0:
            while len(value[str(count)]) == 0 or len(value[str(count)]) == 1:
                value.pop(str(count))
                count = count - 1
                while sudoku[count // 9][count % 9] != 0:
                    if str(count) in value:
                        value.pop(str(count))
                    count = count - 1
            value[str(count)].pop(0)
            continue
        sudoku_solve[count // 9][count % 9] = value[str(count)][0]
        count = count + 1
    return sudoku_solve


