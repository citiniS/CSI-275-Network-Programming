"""
Don't forget your docstrings!
"""
import socket
import ssl

HOST = 'localhost'  # IP of server
PORT = 7778         # Port of server

def create_socket(host, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    return connection

def send_messages():
    """Collect text from the user and send it to our server."""
    user_input = ""

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations("srv_cert.crt")
    context.load_cert_chain("cli_cert.crt", "cli_key.key")
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    ssl_sock = context.wrap_socket(sock, server_side=False, server_hostname="localhost")
    while user_input != "done":
        user_input = input("Please enter a message, or 'done' to exit.")

        encoded_message = user_input.encode('ascii')

        ssl_sock.sendall(encoded_message)

    ssl_sock.shutdown(socket.SHUT_WR)
    ssl_sock.close()

def main():
    """Call send_messages to start our message loop."""
    send_messages()

if __name__ == "__main__":
    main()

