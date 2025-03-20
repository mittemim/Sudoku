import json
import os

class RecordsManager:
    def __init__(self, filename="records.json"):
        """
        Инициализирует менеджер рекордов.
        :param filename: Имя файла для хранения рекордов.
        """
        self.filename = filename
        self.records = self.load_records()

    def load_records(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}
        else:
            return {}

    def save_records(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.records, file, indent=4, ensure_ascii=False)

    def update_record(self, difficulty, score, time_taken):
        """
        Обновляет рекорд для заданного уровня сложности, если текущий счёт выше.
        :param difficulty: Уровень сложности.
        :param score: Текущий счёт.
        :param time_taken: Затраченное время.
        :return: True, если рекорд обновлён, иначе False.
        """
        if difficulty not in self.records or score > self.records[difficulty]["score"]:
            self.records[difficulty] = {"score": score, "time": time_taken}
            self.save_records()
            return True
        return False

    def get_record(self, difficulty):
        """
        Возвращает рекорд для заданного уровня сложности.
        :param difficulty: Уровень сложности.
        :return: Словарь с рекордом или None, если рекорда нет.
        """
        return self.records.get(difficulty, None)
