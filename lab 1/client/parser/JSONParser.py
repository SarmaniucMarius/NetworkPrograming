import json


class JSONParser:
    def parse(self, json_data):
        data_list = list(json_data)
        data_length = len(data_list)
        if data_list[data_length - 3] == ",":
            data_list[data_length - 3] = " "
            json_data = "".join(data_list)
        return json.loads(json_data)
