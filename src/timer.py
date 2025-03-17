import time

class Timer:
    def __init__(self, label):
        """
        Инициализирует таймер.
        :param label: Tkinter Label для отображения времени.
        """
        self.label = label
        self.start_time = None
        self.running = False

    def start(self):
        """
        Запускает таймер и начинает обновлять метку времени.
        """
        self.start_time = time.time()
        self.running = True
        self.update()

    def stop(self):
        """
        Останавливает таймер и возвращает общее время в секундах.
        """
        self.running = False
        if self.start_time is not None:
            elapsed = int(time.time() - self.start_time)
            return elapsed
        return 0

    def update(self):
        if self.running:
            current_time = int(time.time() - self.start_time)
            self.label.config(text=f"Время: {current_time} сек")
            self.label.after(1000, self.update)
