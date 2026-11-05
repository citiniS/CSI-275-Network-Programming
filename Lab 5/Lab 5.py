"""Student code for Lab 5.

Create code in python to encode a message to send back
to a client that would sort the numbers given

Author: Yin Bo Chen
Class: CSI-275-01
Assignment: Lab 5 -- Sorting Server

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)

Champlain College CSI-235, Spring 2019
The following code was written by Joshua Auerbach (jauerbach@champlain.edu)
"""

import socket
#from ctypes.macholib.dyld import dyld_library_path

HOST = "localhost"
PORT = 20000
ERROR_MESSAGE = "ERROR"

class SortServer:
    """Don't forget your docstring!"""

    def __init__(self, host, port):
        """
        Initializes the SortServer class with the given host and port.

        Args:
            host (str): The server's host address.
            port (int): The server's port number.
        """
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        addr_tuple = (self.host, self.port)
        self.connection.bind(addr_tuple)
        pass

    def run_server(self):
        """
        Runs the server, and listens for incoming client connections,
        and processes messages containing lists of numbers.

        The server accepts the following commands from the client:
            - A string starting with 'LIST' and continues with either float or ints as a string,
            and if the string contains '|' the end of the string, it will check for 3 different characters
            to see how it will be sorted  'a' for ascending oder, 'd' for descending order,
            or 's' for sorting alphabetically.
            - Invalid input results in an error message being sent back to the client as 'ERROR'.
        """
        self.connection.listen(20)

        while True:
            cli_sock, address = self.connection.accept()
            while True:
                data = cli_sock.recv(4096)
                if not data:
                    break
                exit_bool = False
                message = data.decode('ascii')
                number_string = ""
                test_string = message
                sort_char = ""
                if "LIST" in message:
                    if "|" in message:
                        test_string = test_string[5:-2]
                        sort_char = message[-1]
                        if sort_char not in ("d", "s", "a"):
                            exit_bool = True
                    else:
                        test_string = message[5:]
                        if len(test_string[4:]) == 0:
                            exit_bool = True
                    if any(char.isalpha() for char in test_string):
                        exit_bool = True
                    else:
                        for number in test_string:
                            number_string += number
                else:
                    exit_bool = True
                number_list = number_string.split(" ")
                real_number_list = []
                for number in number_list:
                    try:
                        real_number_list.append(int(number))
                    except ValueError:
                        try:
                                real_number_list.append(float(number))
                        except ValueError:
                            exit_bool = True
                            break
                if exit_bool:
                    cli_sock.sendall(ERROR_MESSAGE.encode('ascii'))
                else:
                    if sort_char == "d":
                        real_number_list.sort(reverse=True)
                        sorted_string = "SORTED"
                        for numbers in real_number_list:
                            string_number = str(numbers)
                            sorted_string += " " + string_number
                        cli_sock.sendall(sorted_string.encode('ascii'))
                    elif sort_char == "a":
                        real_number_list.sort()
                        sorted_string = "SORTED"
                        for numbers in real_number_list:
                            string_number = str(numbers)
                            sorted_string += " " + string_number
                        cli_sock.sendall(sorted_string.encode('ascii'))
                    elif sort_char == "s":
                        string_number_list = []
                        for number in real_number_list:
                            string_number_list.append(str(number))
                        string_number_list.sort()
                        sorted_num_string = "SORTED " + " ".join(string_number_list)
                        cli_sock.sendall(sorted_num_string.encode('ascii'))
                    else:
                        real_number_list.sort()
                        sorted_string = "SORTED"
                        for numbers in real_number_list:
                            string_number = str(numbers)
                            sorted_string += " " + string_number
                        cli_sock.sendall(sorted_string.encode('ascii'))

if __name__ == "__main__":
    server = SortServer(HOST, PORT)
    server.run_server()