"""Student code for CSI-270-01 Final Project.

Author: Yin Bo Chen
Class: CSI-275-01

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)

"""

import socket
import threading
import json

HOST = "localhost"
SEND_PORT = 7778
RECEIVE_PORT = 7779

def choose_name():
    """Prompt the user for a username"""
    username_input = ""
    while username_input == "":
        username_input = input("Please enter a username: ")
    return username_input

def recvall(connection, length, data = b''):
    """
    Collects at least the advertised amount of data from the client.
    if it doesn't, return a 'Length Error' message

    Args:
        connection (socket.socket): The connection's address.
        length (int): The advertised length of the string
        data (bytes): the data sent in bytes
    """
    while len(data) < length:
        more = connection.recv(length - len(data))
        if not more:  # Check for disconnection
            print("Connection closed unexpectedly")
            return None
        data += more
    return data

def encode_message(msg_data):
    """
    Encode message received from user into JSON

    Args:
        msg_data (list[str]): list containing strings of the message type, user's username, and message to send
    """
    json_data = json.dumps(msg_data)
    json_bytes = json_data.encode('utf-8')
    msg_length = len(json_bytes)
    length_prefix = msg_length.to_bytes(4, 'big')
    json_msg = length_prefix + json_bytes
    return json_msg


def receive_loop(recv_conn, username):
    """
    Listens for and displays incoming chat messages.

    Args:
        recv_conn (socket.pyi): Server connection
        username (str): User's name

    """
    start_msg = ["START", username]
    recv_conn.sendall(encode_message(start_msg))

    while True:
        try:
            length_bytes = recvall(recv_conn, 4)
            msg_length = int.from_bytes(length_bytes, 'big')
            data = recvall(recv_conn, msg_length)

            json_msg = data.decode('utf-8')
            if not json_msg:
                break
            message = json.loads(json_msg)

            msg_type = message[0]
            if msg_type == "BROADCAST":
                sender, text = message[1], message[2]
                print(f"\n{sender}: {text}")

            elif msg_type == "PRIVATE":
                sender, text = message[1], message[2]
                print(f"\n{sender}(private): {text}")

            elif msg_type == "START":
                sender, text = message[1], message[2]
                print(f"\n{sender} {text}")

            elif msg_type == "EXIT":
                sender, text = message[1], message[2]
                print(f"\n{sender} {text}")

        except (ConnectionResetError, ConnectionAbortedError):
            break
    recv_conn.close()

def message(username, socket_conn):
    """
    Handles sending chat messages through a socket connection.

    Args:
        username (str): The current user's name
        socket_conn (socket.pyi): The active socket connection to the server
    """
    message_type_input = ""
    message_input = ""
    private_message_input = ""

    while True:
        message_type_input = ""
        message_input = ""
        private_message_input = ""

        message_type_input = input( "Please enter the message type you want to send:"
                                    " <BROADCAST, PRIVATE> OR <EXIT> to exit: ")

        if message_type_input == "EXIT":
            msg_data = ["EXIT", username]
            socket_conn.sendall(encode_message(msg_data))
            socket_conn.close()
            return

        elif message_type_input == "BROADCAST":
            while message_input == "":
                message_input = input("Please enter the message you want to broadcast: ")

            msg_data = ["BROADCAST", username, message_input]
            socket_conn.sendall(encode_message(msg_data))

        elif message_type_input == "PRIVATE":
            while private_message_input == "":
                private_message_input = input("Please enter the username of the person you want to message: ")

            while message_input == "":
                message_input = input("Please enter the message you want to send: ")

            msg_data = ["PRIVATE", username, message_input, private_message_input]
            socket_conn.sendall(encode_message(msg_data))

def main():
    username = choose_name()

    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.connect((HOST, SEND_PORT))

    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receive_socket.connect((HOST, RECEIVE_PORT))

    receive_thread = threading.Thread(target=receive_loop, args=(receive_socket, username))
    receive_thread.start()

    message(username, send_socket)

    send_socket.close()
    receive_socket.close()

if __name__ == "__main__":
    main()