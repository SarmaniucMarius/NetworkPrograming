import socket
import json
import threading
from server.Error import Error
from server.ThreadState import ThreadState

HOST, PORT = "0.0.0.0", 8888
database_columns = ["id", "first_name", "last_name", "card_number", "card_balance",
                    "card_currecny", "bitcoin_address", "email", "gender", "ip_address",
                    "username", "created_account_data", "organization", "full_name",
                    "employee_id"]
commands = ["select", "quit"]


def init_listen_socket():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
    return listen_socket


def tokenize_data(data):
    tokens = []
    cur = 0
    while data[cur] != '\n':
        char = data[cur]
        if char.isalpha() is True:
            start = cur
            while char.isspace() is not True:
                cur += 1
                char = data[cur]
            tokens.append(data[start:cur])
        cur += 1
    return tokens


def get_data_as_string(column):
    with open('data.txt', 'r') as f:
        file_data = f.read()
    database_data = json.loads(file_data)
    column_data = database_data[column]
    data_str = str(column_data)
    data_str += '\r\n'
    return data_str


def func_quit(state, tokens):
    state.connection.close()
    state.running = False


def func_select(state, tokens):
    error = Error(state.connection)
    if len(tokens) == 2:
        requested_column = tokens[1]
        if requested_column in database_columns:
            data = get_data_as_string(requested_column)
            state.connection.sendall(data.encode())
        else:
            error.column_error(requested_column)
    else:
        error.request_error()


func = {
    'quit': func_quit,
    'select': func_select
}


def server_request(connection):
    state = ThreadState(connection)
    initial_message = """commands: 
quit - closes connection
select column-name - returns values from that column
"""
    connection.sendall(initial_message.encode())
    error = Error(connection)
    while state.running is True:
        request_data = connection.recv(1024).decode()
        tokens = tokenize_data(request_data)
        if len(tokens) != 0:
            command = tokens[0]
            if command in commands:
                func[command](state, tokens)
            else:
                error.command_error(command)
        else:
            error.request_error()


if __name__ == "__main__":
    socket = init_listen_socket()
    print(f'Serving HTTP on port {PORT} ... ')
    while True:
        client_connection, client_address = socket.accept()
        thread = threading.Thread(target=server_request, args=(client_connection,))
        thread.start()
