import unittest
from src.sudoku_generator import generate_sudoku

class TestSudokuGenerator(unittest.TestCase):
    def test_generate_complete_puzzle(self):
        # Генерируем паззл с 36 пустыми ячейками (легкий уровень)
        puzzle = generate_sudoku(36)
        self.assertEqual(len(puzzle), 9)
        for row in puzzle:
            self.assertEqual(len(row), 9)

if __name__ == "__main__":
    unittest.main()
