import time

class Timer:
    def __init__(self, label):
        self.label = label
        self.start_time = 0
        self.is_running = False

    def start(self):
        self.start_time = time.time()
        self.is_running = True
        self.update_label()

    def stop(self):
        self.is_running = False
        if self.start_time != 0:
            end_time = time.time()
            total_time = int(end_time - self.start_time)
            return total_time
        return 0

    def update_label(self):
        if self.is_running:
            current_time = int(time.time() - self.start_time)
            self.label.config(text=f"Time: {current_time} sec")
            self.label.after(1000, self.update_label)
