import json
import os

class RecordsManager:
    def __init__(self, filename="records.json"):

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

        if difficulty not in self.records or score > self.records[difficulty]["score"]:
            self.records[difficulty] = {"score": score, "time": time_taken}
            self.save_records()
            return True
        return False

    def get_record(self, difficulty):

        return self.records.get(difficulty, None)
