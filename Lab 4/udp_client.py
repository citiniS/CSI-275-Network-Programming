"""Student code for Lab 4.

Create code in python to encode a message to send to
a server that would echo back the same message

Author: Yin Bo Chen
Class: CSI-275-01
Assignment: Lab 4 -- UDP Sockets

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
import constants
import random


class TimeOutError(Exception):
    """Exception raised for timeout errors."""

    pass


class UDPClient:
    """Return whether the given ip_address is a valid IPv4 address or not.

    Methods:
        send_message_by_character(self, message):
            Sends a message by single characters.
    """

    def __init__(self, host, port, boolean=False):
        """Initialize the UDPClient class.

        Takes the string that was inputted and sends
        an encoded version to a UDP server which
        should send the message back. If it takes
        too long for the message to come back,
        a TimeOutError is raised.

        Parameter:
            host (str): Host IP address
            port (int): echo port number
            boolean (optional bool): checks to see
            if request id is needed when sending message
            to server (default is False)
        """
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.boolean = boolean

    def send_message_by_character(self, message):
        """Send an encoded message character by character.

        Args:
            message (str): the message you want to send

        Returns:
            answer (str): decoded string that was received from
            the server
        """
        if not self.boolean:
            answer = ""
            for character in message:
                wait_time = constants.INITIAL_TIMEOUT
                self.connection.settimeout(wait_time)
                while True:
                    try:
                        self.connection.sendto(character.encode("ascii"),
                                               (self.host, self.port))
                        response, address = self.connection.recvfrom(4096)
                        result = response.decode('ascii')
                        answer += result
                        break
                    except socket.timeout:
                        if wait_time < constants.MAX_TIMEOUT:
                            wait_time *= 2
                            self.connection.settimeout(wait_time)
                        else:
                            raise TimeOutError
            return answer
        else:
            answer = ""
            for character in message:
                request_id = random.randint(0, constants.MAX_ID)
                formatted_message = f"{request_id}|{character}"
                wait_time = constants.INITIAL_TIMEOUT
                self.connection.settimeout(wait_time)
                while True:
                    try:
                        self.connection.sendto(formatted_message.encode
                                               ("ascii"),
                                               (self.host, self.port))
                        response, address = self.connection.recvfrom(4096)
                        result = response.decode('ascii')
                        temp_variable = result.split("|")
                        response_id = temp_variable[0]
                        response_character = temp_variable[1]
                        if int(response_id) == request_id:
                            answer += response_character
                            break
                        else:
                            continue
                    except socket.timeout:
                        if wait_time < constants.MAX_TIMEOUT:
                            wait_time *= 2
                            self.connection.settimeout(wait_time)
                        else:
                            raise TimeOutError
            return answer


def main():
    """Run some basic tests on the required functionality.

    for more extensive tests run the autograder!
    """
    client = UDPClient(constants.HOST, constants.ECHO_PORT)
    print(client.send_message_by_character("hello world"))

    client = UDPClient(constants.HOST, constants.REQUEST_ID_PORT, True)
    print(client.send_message_by_character("hello world"))


if __name__ == "__main__":
    main()
