import tkinter as tk
from tkinter import messagebox, Frame
from sudoku_generator import generate_sudoku
from timer import Timer
from score import ScoreManager
from sudoku_solver import solve_sudoku  # Импортируем решатель
from records_manager import RecordsManager

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Судоку")

        # Фрейм управления
        control_frame = tk.Frame(master)
        control_frame.pack(side=tk.TOP, pady=5)

        self.difficulty = tk.StringVar(master)
        self.difficulty.set("Средний")
        difficulties = ["Легкий", "Средний", "Сложный", "Миссия невыполнима"]
        tk.OptionMenu(control_frame, self.difficulty, *difficulties, command=self.new_game).pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="Новая игра", command=lambda: self.new_game(self.difficulty.get())).pack(side=tk.LEFT, padx=5)
        self.check_button = tk.Button(control_frame, text="Проверить", command=self.check_solution)
        self.check_button.pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Решить", command=self.solve_puzzle).pack(side=tk.LEFT, padx=5)
          # Новая кнопка "Рекорды" для специального режима решения судоку
        tk.Button(control_frame, text="Рекорды", command=self.show_records).pack(side=tk.LEFT, padx=5)

        # Панель для отображения времени и счёта
        info_frame = tk.Frame(master)
        info_frame.pack(side=tk.TOP, pady=5)
        self.timer_label = tk.Label(info_frame, text="Время: 0 сек", font=('Arial', 14))
        self.timer_label.pack(side=tk.LEFT, padx=10)
        self.score_label = tk.Label(info_frame, text="Счёт: 1000", font=('Arial', 14))
        self.score_label.pack(side=tk.LEFT, padx=10)

        # Создаем объекты таймера, менеджера очков и менеджера рекордов
        self.timer = Timer(self.timer_label)
        self.score_manager = ScoreManager()
        self.records_manager = RecordsManager()

        # Фрейм игрового поля
        self.game_frame = tk.Frame(master, bg='black')
        self.game_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.new_game(self.difficulty.get())

    def new_game(self, difficulty):
        # Останавливаем предыдущий таймер, если он был запущен
        if hasattr(self, 'timer'):
            self.timer.running = False

        for widget in self.game_frame.winfo_children():
            widget.destroy()

        mapping = {"Легкий": 36, "Средний": 46, "Сложный": 56, "Миссия невыполнима": "Миссия невыполнима"}
        empties = mapping.get(difficulty, 46)
        self.game_board = generate_sudoku(empties)

        self.score_manager = ScoreManager()
        self.score_label.config(text=f"Счёт: {self.score_manager.get_score()}")

        self.timer = Timer(self.timer_label)
        self.timer.start()

        # Создаем блоки 3x3
        blocks = [[tk.Frame(self.game_frame, borderwidth=2, relief="groove", bg='black') for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                blocks[i][j].grid(row=i, column=j, padx=2, pady=2)

        self.widgets = []
        for i in range(9):
            row = []
            for j in range(9):
                block = blocks[i // 3][j // 3]
                entry = tk.Entry(block, width=2, font=('Arial', 24), justify='center', borderwidth=1)
                entry.grid(row=i % 3, column=j % 3, padx=2, pady=2)
                if self.game_board[i][j] != 0:
                    entry.insert(tk.END, str(self.game_board[i][j]))
                    entry.config(state='readonly', disabledforeground='black', readonlybackground='#d3d3d3')
                else:
                    entry.config(bg='white')
                    entry.bind("<KeyRelease>", self.validate_entry)
                row.append(entry)
            self.widgets.append(row)

    def validate_entry(self, event):
        widget = event.widget
        text = widget.get()
        if text and (not text.isdigit() or int(text) < 1 or int(text) > 9):
            widget.delete(0, tk.END)
            widget.config(bg='#fa7373')
        else:
            widget.config(bg='white')
            
    def check_value(self, row, col, num):
        """
        Проверяет, соответствует ли значение num в ячейке (row, col) правилам Судоку:
        - Число не должно повторяться в строке.
        - Число не должно повторяться в столбце.
        - Число не должно повторяться в блоке 3x3.
        Возвращает True, если значение корректно, иначе False.
        """
        # Проверка строки
        for x in range(9):
            if x != col:
                val = self.widgets[row][x].get()
                if val == str(num):
                    return False
        # Проверка столбца
        for y in range(9):
            if y != row:
                val = self.widgets[y][col].get()
                if val == str(num):
                    return False
        # Проверка блока 3x3
        startRow, startCol = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                cur_row = startRow + i
                cur_col = startCol + j
                if cur_row == row and cur_col == col:
                    continue
                val = self.widgets[cur_row][cur_col].get()
                if val == str(num):
                    return False
        return True

    def finish_game(self):
        elapsed = self.timer.stop()
        bonus = max(0, 100 - elapsed)
        self.score_manager.add_bonus(bonus)
        self.score_label.config(text=f"Счёт: {self.score_manager.get_score()}")
        new_record = self.records_manager.update_record(self.difficulty.get(), self.score_manager.get_score(), elapsed)
        record_msg = "\nНовый рекорд!" if new_record else ""
        messagebox.showinfo("Результат", f"Поздравляем! Вы решили Судоку за {elapsed} сек.\nВаш итоговый счёт: {self.score_manager.get_score()}{record_msg}")

    def show_records(self):
        record = self.records_manager.get_record(self.difficulty.get())
        if record:
            messagebox.showinfo("Рекорды", f"Уровень: {self.difficulty.get()}\nЛучший счёт: {record['score']}\nВремя: {record['time']} сек")
        else:
            messagebox.showinfo("Рекорды", f"Уровень: {self.difficulty.get()}\nПока рекордов нет.")

    
  def check_solution(self):
        """
        Проверяет все ячейки игрового поля:
        - Сначала проверяется, что значение в ячейке является числом от 1 до 9.
        - Затем вызывается check_value(), которая проверяет уникальность числа в строке, столбце и блоке 3x3.
        Если какая-либо ячейка нарушает правила, она подсвечивается красным.
        """
        correct = True
        for i, row in enumerate(self.widgets):
            for j, widget in enumerate(row):
                try:
                    val = int(widget.get())
                    # Если число не в диапазоне 1-9 или нарушает уникальность, подсвечиваем красным
                    if val < 1 or val > 9 or not self.check_value(i, j, val):
                        widget.config(bg='#fa7373')
                        correct = False
                    else:
                        widget.config(bg='white')
                except ValueError:
                    widget.config(bg='#fa7373')
                    correct = False
        if correct:
            self.finish_game()
        else:
            messagebox.showwarning("Результат", "Найдены ошибки. Неверные ячейки подсвечены красным.")

    def solve_puzzle(self):
        """
        Считывает текущую матрицу из виджетов, решает судоку и обновляет интерфейс.
        Если решение найдено, заменяет введенные данные на решение.
        """
        board = []
        for i, row in enumerate(self.widgets):
            current_row = []
            for j, widget in enumerate(row):
                text = widget.get()
                try:
                    num = int(text) if text != "" else 0
                except ValueError:
                    num = 0
                current_row.append(num)
            board.append(current_row)

        if solve_sudoku(board):
            # Если решение найдено, обновляем виджеты с решением
            for i, row in enumerate(self.widgets):
                for j, widget in enumerate(row):
                    widget.config(state='normal')
                    widget.delete(0, tk.END)
                    widget.insert(tk.END, str(board[i][j]))
                    widget.config(state='readonly', disabledforeground='black', readonlybackground='#d3d3d3')
            messagebox.showinfo("Результат", "Судоку решено!")
        else:
            messagebox.showerror("Ошибка", "Невозможно решить судоку с текущими данными.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
