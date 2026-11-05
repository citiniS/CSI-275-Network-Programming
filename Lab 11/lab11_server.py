"""Don't forget your docstrings!
"""

import socket, ssl
import _thread

from Tools.scripts.mailerdaemon import emparse_list

HOST = 'localhost'  # IP of server
PORT = 7778         # Port of server

def handler(client_socket, addr):
    """Receive messages and print them to the console."""
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("srv_cert.crt", "srv_key.key")
    context.load_verify_locations("cli_cert.crt")

    ssl_sock = context.wrap_socket(client_socket, server_side=True)
    print(addr)
    while True:
        message = ssl_sock.recv(4096)
        if not message:
            break
        result = message.decode('ascii')
        print(result)
    ssl_sock.close()



if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(20)

    while True:
        client_sock, addr = sock.accept()
        _thread.start_new_thread(handler, (client_sock, addr))