"""Student code for Lab 6.

Create code in python that parses a simple text protocol that tells us how much data is coming.
Messages being sent and received by the server should be in the following format.

Author: Yin Bo Chen
Class: CSI-275-01
Assignment: Lab 6 -- Framing with Length Fields

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

from Tools.demo.mcast import sender

HOST = "localhost"
PORT = 45000

class LengthServer:
    """Create a server that return the length of received strings."""

    def __init__(self, host, port):
        """
        Initializes the SortServer class with the given host and port.

        Args:
            host (str): The server's host address.
            port (int): The server's port number.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)

    def recvall(self, connection, length, data = b''):
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
            if not more:
                raise EOFError('expected %d bytes but only received'
                               ' %d bytes before the socket closed'
                               % (length, len(data)))

            data += more
        return data

    def calc_length(self):
        """
        Listens for client connections on the provided socket, reads the length of the incoming data,
        receives the specified number of bytes, and verifies the length. If the length is correct,
        it responds with the message "I received X bytes.", where X is the length of the received data.
        If there's a length incorrect, it sends "Length Error" to the client.
        """
        self.socket.bind(self.addr)
        self.socket.listen()
        message = ""
        sending_string = ""
        testing = "CSI-275".encode('ascii')

        while True:
            conn, _ = self.socket.accept()
            # int recv(char* buffer, size_t buffer_len);
            # // Writes up to buffer_len bytes to buffer.
            # Making recv() really small to test recvall()!
            msg_raw = conn.recv(8)
            # first four bytes are message length.
            msg_len = int.from_bytes(msg_raw[:4], 'big')

            msg_body = msg_raw[4:msg_len + 4]
            try:
                msg_body = self.recvall(conn, msg_len, msg_body)
            except EOFError:
                error_message = "Length Error"
                error_string = len(error_message).to_bytes(4, 'big') + error_message.encode('ascii')
                conn.sendall(error_string)
            if msg_body:
                message = f"I received {msg_len} bytes."
                sending_string = len(message).to_bytes(4, 'big') + message.encode('ascii')
                conn.sendall(sending_string)
            print(testing)
            conn.close()


if __name__ == "__main__":
    server = LengthServer(HOST, PORT)
    server.calc_length()