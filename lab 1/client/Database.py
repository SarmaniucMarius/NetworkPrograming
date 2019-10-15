from threading import Lock
import json


class Database:
    def __init__(self):
        self.data = {}
        self.lock = Lock()

    def add(self, record):
        with self.lock:
            for key in record:
                value = record[key]
                if key not in self.data:
                    self.data[key] = []
                if value is not None:
                    self.data[key].append(str(value))

    def save_data(self, file):
        with open(file, "w") as f:
            json_data = json.dumps(self.data)
            f.write(json_data)
