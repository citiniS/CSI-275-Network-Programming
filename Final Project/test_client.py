"""DONT FORGET DOC STINGS.
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
    json_data = json.dumps(msg_data)
    json_bytes = json_data.encode('utf-8')
    msg_length = len(json_bytes)
    length_prefix = msg_length.to_bytes(4, 'big')
    json_msg = length_prefix + json_bytes
    return json_msg


def receive_loop(recv_conn, username):
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
    Menu-based message input function adapted from the provided code.
    This handles the user interface for message creation and sending.
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