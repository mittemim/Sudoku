import unittest
from src.sudoku_generator import generate_sudoku

class TestSudokuGenerator(unittest.TestCase):
    def test_generate_complete_puzzle(self):
        # Генерируем паззл с 36 пустыми ячейками (легкий уровень)
        puzzle = generate_sudoku(36)
        self.assertEqual(len(puzzle), 9)
        for row in puzzle:
            self.assertEqual(len(row), 9)
    
    def test_special_difficulty(self):
        # Проверяем уровень "Миссия невыполнима"
        puzzle = generate_sudoku("Миссия невыполнима")
        self.assertEqual(puzzle[0][0], 8)
        self.assertIn(0, puzzle[0])

if __name__ == "__main__":
    unittest.main()
