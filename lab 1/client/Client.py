import logging
import requests
import threading
import time
from client.parser.ParserFactory import ParserFactory
from client.Database import Database

home_url = "http://0.0.0.0:5000"


def make_request(url, header=None):
    response = requests.get(url, headers=header)
    return response.json()


def request_route(route, header, storage):
    route_response = make_request(home_url + route, header)
    traverse(route_response, header, storage)


def traverse(response, header, storage):
    if "data" in response:
        response_data = response["data"]
        data_type = 'json'
        if "mime_type" in response:
            data_type = response["mime_type"]
        parser = ParserFactory.get_parser(data_type)
        data = parser.parse(response_data)
        for record in data:
            storage.add(record)

    if "link" in response:
        links = response["link"]
        threads = list()
        for item in links.items():
            thread = threading.Thread(target=request_route, args=(item[1], header, storage))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()


if __name__ == "__main__":
    start_time = time.time()
    register_response = make_request(home_url + "/register")
    _format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=_format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    access_header = {"X-Access-Token": register_response["access_token"]}
    home_response = make_request(home_url + "/home", access_header)

    database = Database()
    traverse(home_response, access_header, database)
    database.save_data("data.txt")

    print("%s seconds" % (time.time() - start_time))
