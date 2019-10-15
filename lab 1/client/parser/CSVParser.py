from io import StringIO
import csv


class CSVParser:
    def parse(self, csv_data):
        f = StringIO(csv_data)
        csv_file_data = csv.DictReader(f)
        data = []
        for record in csv_file_data:
            data.append(record)
        f.close()
        return data
