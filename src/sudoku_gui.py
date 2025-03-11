import tkinter as tk
from tkinter import messagebox, Frame
from sudoku_generator import generate_sudoku

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Судоку")

        # Фрейм управления: выбор сложности, кнопки
        control_frame = tk.Frame(master)
        control_frame.pack(side=tk.TOP, pady=5)

        self.difficulty = tk.StringVar(master)
        self.difficulty.set("Средний")
        difficulties = ["Легкий", "Средний", "Сложный"]
        tk.OptionMenu(control_frame, self.difficulty, *difficulties, command=self.new_game).pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="Новая игра", command=lambda: self.new_game(self.difficulty.get())).pack(side=tk.LEFT, padx=5)
        self.check_button = tk.Button(control_frame, text="Проверить", command=self.check_solution)
        self.check_button.pack(side=tk.RIGHT, padx=5)

         # Панель для отображения дополнительной информации
        info_frame = tk.Frame(master)
        info_frame.pack(side=tk.TOP, pady=5)
        self.info_label = tk.Label(info_frame, text="Введите числа в пустые ячейки", font=('Arial', 14))
        self.info_label.pack()
        
        # Фрейм игрового поля
        self.game_frame = tk.Frame(master, bg='black')
        self.game_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.new_game(self.difficulty.get())

    def new_game(self, difficulty):
        # Очистка предыдущего поля
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        # Определяем количество пустых ячеек
        mapping = {"Легкий": 36, "Средний": 46, "Сложный": 56}
        empties = mapping.get(difficulty, 46)
        self.game_board = generate_sudoku(empties)

        # Создаем блоки 3x3
        blocks = [[Frame(self.game_frame, borderwidth=1, relief="groove", bg='black') for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                blocks[i][j].grid(row=i, column=j, padx=1, pady=1)

        # Создаем виджеты Entry для каждой ячейки
        self.widgets = []
        for i in range(9):
            row = []
            for j in range(9):
                block = blocks[i // 3][j // 3]
                entry = tk.Entry(block, width=2, font=('Arial', 24), justify='center', borderwidth=1)
                entry.grid(row=i % 3, column=j % 3, padx=1, pady=1)
                if self.game_board[i][j] != 0:
                    entry.insert(tk.END, str(self.game_board[i][j]))
                    entry.config(state='readonly', disabledforeground='black')
                row.append(entry)
            self.widgets.append(row)

    def check_solution(self):
        correct = True
        for i, row in enumerate(self.widgets):
            for j, widget in enumerate(row):
                try:
                    val = int(widget.get())
                    # Простейшая проверка: число от 1 до 9
                    if val < 1 or val > 9:
                        widget.config(bg='#fa7373')
                        correct = False
                    else:
                        widget.config(bg='white')
                except ValueError:
                    widget.config(bg='#fa7373')
                    correct = False
        if correct:
            messagebox.showinfo("Результат", "Поздравляем! Вы правильно решили Судоку!")
        else:
            messagebox.showwarning("Результат", "Найдены ошибки. Неверные ячейки подсвечены красным.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
