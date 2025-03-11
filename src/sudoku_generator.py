import random

def generate_sudoku(empties):
       if empties == "Миссия невыполнима":      
              return [
                   [8, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 3, 6, 0, 0, 0, 0, 0],
                   [0, 7, 0, 0, 9, 0, 2, 0, 0],
                   [0, 5, 0, 0, 0, 7, 0, 0, 0],
                   [0, 0, 0, 0, 4, 5, 7, 0, 0],
                   [0, 0, 0, 1, 0, 0, 0, 3, 0],
                   [0, 0, 1, 0, 0, 0, 0, 6, 8],
                   [0, 0, 8, 5, 0, 0, 0, 1, 0],
                   [0, 9, 0, 0, 0, 0, 4, 0, 0]
              ]

       base = 3  # Размер блока (3x3)
       side = base * base  # Размер стороны доски

    def check(grid, row, col, num):
        # Проверка строки и столбца
        for x in range(side):
            if grid[row][x] == num or grid[x][col] == num:
                return False
        # Проверка блока 3x3
        startRow = base * (row // base)
        startCol = base * (col // base)
        for i in range(base):
            for j in range(base):
                if grid[i + startRow][j + startCol] == num:
                    return False
        return True

    def fill_grid(grid):
        for i in range(side):
            for j in range(side):
                if grid[i][j] == 0:
                    nums = list(range(1, side + 1))
                    random.shuffle(nums)
                    for num in nums:
                        if check(grid, i, j, num):
                            grid[i][j] = num
                            if not any(0 in row for row in grid) or fill_grid(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True

    # Создаём пустую сетку
    grid = [[0 for _ in range(side)] for _ in range(side)]
    fill_grid(grid)

    # Удаляем числа для создания паззла
    for _ in range(empties if isinstance(empties, int) else 36):
        i, j = random.randint(0, side - 1), random.randint(0, side - 1)
        while grid[i][j] == 0:
            i, j = random.randint(0, side - 1), random.randint(0, side - 1)
        grid[i][j] = 0

    return grid

# Пример для ручного тестирования модуля (при выполнении файла напрямую)
if __name__ == "__main__":
    puzzle = generate_sudoku(46)
    for row in puzzle:
        print(row)
