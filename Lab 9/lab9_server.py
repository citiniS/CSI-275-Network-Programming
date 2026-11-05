"""Server code for Lab 9.

Create code in python that listens to a client and sends back based off
the specifications given by the client

Author: Duane Dunston (original author)
Author: Jason Reeves (modified code for CSI-275)
Author: Yin Bo Chen (modified code as student for CSI-275)
Class: CSI-275-01
Assignment: Lab 9 - JSON Client/Server

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
import zlib
from socket import *
import _thread
import time, datetime
import json

HOST = 'localhost'  # IP of server
PORT = 7778         # Port of server


def handler(client_socket, addr):
    """Handler function for socket connections.

    Data submitted must be in the form "[num1 num2 ... numN]",
    where num1 through numN must be integers or floating-point numbers.

    """
    while True:
        # Receive the data
        compressed_data = client_socket.recv(4096)
        if not compressed_data:
            break

        data = zlib.decompress(compressed_data)
        # Decode the data into a list
        data_list = json.loads(data.decode('utf-8'))
        string_list = []
        # Get time of connection
        now = datetime.datetime.now().timestamp()
        now_readable = time.ctime(now)

        # Print data and time of reception
        print(f"{now_readable}: Got {data} from {addr}")

        # Validate data and checks if list starts wth char
        if data_list[0] == "a":
            is_error = False
        elif data_list[0] == "d":
            is_error = False
        elif data_list[0] == "s":
            is_error = False
        else:
            is_error = True

        if not is_error:
            for element in data_list[1:]:
                try:
                    # This will allow numeric data through
                    float(element)
                except ValueError:  # Data is non-numeric
                    print("Value Error")
                    is_error = True

        return_data = ""
        if not is_error:
            # Sort data
            if data_list[0] == "a":
                new_data_list = data_list[1:]
                new_data_list.sort()
            elif data_list[0] == "d":
                new_data_list = data_list[1:]
                new_data_list.sort(reverse=True)
            elif data_list[0] == "s":
                for number in data_list[1:]:
                    string_list.append(str(number))
                new_data_list = string_list
                new_data_list.sort()
            if len(data_list) == 1:
                empty_list = []
                new_data_list = empty_list
            # Return the data to the client
            return_data = json.dumps(new_data_list)
        else:  # Error
            return_data = json.dumps(["ERROR"])

        # Send our response, whatever it may be
        encoded_string = return_data.encode('utf-8')
        compressed_string = zlib.compress(encoded_string)
        print(f"Returning {return_data} to the client")
        client_socket.sendall(compressed_string)


if __name__ == "__main__":
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(20)

    while 1:
        client_sock, addr = sock.accept()
        _thread.start_new_thread(handler, (client_sock, addr))