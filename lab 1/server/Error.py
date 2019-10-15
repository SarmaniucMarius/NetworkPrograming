class Error:
    def __init__(self, connection):
        self.connection = connection

    def request_error(self):
        error_massage = 'Request should look like this: command column-name\n'
        self.connection.sendall(error_massage.encode())

    def command_error(self, command):
        error_massage = 'Command: "' + command + '" does not exist!\n'
        self.connection.sendall(error_massage.encode())

    def column_error(self, column):
        error_massage = 'Requseted column: "' + column + '" does not exist!\n'
        self.connection.sendall(error_massage.encode())
