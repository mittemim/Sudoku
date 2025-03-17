def solve_sudoku(board):
    """
    Решает судоку, используя алгоритм backtracking.
    Изменяет доску (список списков) in-place и возвращает True,
    если решение найдено, иначе False.
    Пустые ячейки обозначаются нулём.
    """
    n = 9

    def find_empty(board):
        for i in range(n):
            for j in range(n):
                if board[i][j] == 0:
                    return i, j  # возвращаем координаты первой пустой ячейки
        return None

    def is_valid(board, num, pos):
        row, col = pos
        # Проверяем строку
        for j in range(n):
            if board[row][j] == num and j != col:
                return False
        # Проверяем столбец
        for i in range(n):
            if board[i][col] == num and i != row:
                return False
        # Проверяем блок 3x3
        box_x = col // 3
        box_y = row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False
        return True

    empty = find_empty(board)
    if not empty:
        return True  # нет пустых ячеек – судоку решено
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0  # откат, если не подходит
    return False
