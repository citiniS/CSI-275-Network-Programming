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

HOST = 'localhost'
READ_PORT = 7778
WRITE_PORT = 7779

client_usernames = {}
lock = threading.Lock()

def recvall(connection, length, data=b''):
    """
    Collects at least the advertised amount of data from the client.

    Args:
        connection (socket.socket): The client socket
        length (int): The advertised length of the data
        data (bytes): Initial data buffer (default empty)

    Returns:
        bytes or None: The received data or None if connection closed
    """
    while len(data) < length:
        more = connection.recv(length - len(data))
        if not more:  # Connection closed
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

def send_message(msg_data):
    """
    Broadcasts a message to all connected clients.

    Args:
        msg_data (list[str]): list containing strings of the message type, name of user who sent it, and message to send
    """
    with lock:
        disconnect_clients = []
        for name, cli_sock in client_usernames.items():
            try:
                cli_sock.sendall(encode_message(msg_data))
            except:
                disconnect_clients.append(name)
        for name in disconnect_clients:
            del client_usernames[name]

def client_message(cli_sock, cli_addr):
    """
    Handles incoming messages from a client.

    Args:
        cli_sock (socket.pyi): Client's socket connection
        cli_addr (tuple): Client's address information
    """
    while True:
        try:
            length_bytes = recvall(cli_sock, 4)
            if length_bytes is None:
                break
            msg_length = int.from_bytes(length_bytes, 'big')
            data = recvall(cli_sock, msg_length)
            json_data = data.decode('utf-8')
            message = json.loads(json_data)
            if not message:
                break
            msg_type = message[0]
            if msg_type == "START":
                client_name = message[1]
                server = "SERVER"
                message_to_send = f"{client_name} has entered"
                send_message(["START", server, message_to_send])
            elif msg_type == "BROADCAST":
                client_name = message[1]
                message_to_send = message[2]
                send_message(["BROADCAST", client_name, message_to_send])
            elif msg_type == "PRIVATE":
                client_name = message[1]
                message_to_send = message[2]
                reciever = message[3]
                with lock:
                    if reciever in client_usernames:
                        client_usernames[reciever].sendall(encode_message(["PRIVATE",client_name, message_to_send]))
                        client_usernames[client_name].sendall(encode_message(["PRIVATE",client_name, message_to_send]))
                    else:
                        server = "Server"
                        message_to_send = f"{reciever} does not exist"
                        client_usernames[client_name].sendall(encode_message(["PRIVATE", server, message_to_send]))
            elif msg_type == "EXIT":
                client_name = message[1]
                message_to_send = "has left"
                with lock:
                    if client_name in client_usernames:
                        del client_usernames[client_name]
                send_message(["EXIT", client_name, message_to_send])
        except (ConnectionResetError, ConnectionAbortedError):
            break
    cli_sock.close()

def start_loop(write_cli_sock, write_cli_addr):
    """
     andles new client connections.

    Args:
        write_cli_sock (socket.pyi): Client's socket for writing
        write_cli_addr (tuple): Client's address information
    """
    length_bytes = recvall(write_cli_sock, 4)
    if length_bytes is None:
        write_cli_sock.close()
    msg_length = int.from_bytes(length_bytes, 'big')
    data = recvall(write_cli_sock, msg_length)
    json_data = data.decode('utf-8')
    message = json.loads(json_data)

    if message[0] != "START":
        write_cli_sock.close()
    username = message[1]
    with lock:
        client_usernames[username] = write_cli_sock

    send_message(["BROADCAST", "SERVER", f"{username} has joined the chat."])

def reading_thread(read_socket):
    """
    Accepts new client connections for reading messages.

    Args:
        read_socket (socket.pyi): Server socket listening for connections
    """
    while True:
        read_cli_sock, read_cli_addr = read_socket.accept()
        read_cli_thread = threading.Thread(target=client_message, args=(read_cli_sock, read_cli_addr))
        read_cli_thread.start()

def writing_thread(write_socket):
    """
    Accepts new client connections for writing messages.

    Args:
        write_socket (socket.pyi): Server socket listening for connections
    """
    while True:
        write_cli_sock, write_cli_addr = write_socket.accept()
        write_cli_thread = threading.Thread(target=start_loop, args=(write_cli_sock, write_cli_addr))
        write_cli_thread.start()


def main():
    read_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    read_socket.bind((HOST, READ_PORT))
    read_socket.listen()

    write_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    write_socket.bind((HOST, WRITE_PORT))
    write_socket.listen()

    read_thread = threading.Thread(target=reading_thread, args=(read_socket,))
    read_thread.start()

    write_thread = threading.Thread(target=writing_thread, args=(write_socket,))
    write_thread.start()

    read_thread.join()
    write_thread.join()

    read_socket.close()
    write_socket.close()

if __name__ == "__main__":
    main()