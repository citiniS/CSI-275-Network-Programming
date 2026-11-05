"""Student code for Lab 9.

Create code in python to covert an unsorted list from user input
into JSON, then compress it using zlib before sending to a server

Author: Yin Bo Chen
Class: CSI-275-01
Assignment: Lab 9 -- JSON Client/Server

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
import json
import socket
import zlib


def build_list():
    """Collect input from the user and return it as a list.

    Only numeric input will be included; strings are rejected.
    """
    #Create a list to store our numbers
    unsorted_list = []

    # Create a variable for input
    user_input = ""
    user_input_sorting = ""

    while user_input_sorting != "done":
        user_input_sorting = input(str("Please specify how the list will be sorted with a, d, or s. or done to stop."))
        if user_input_sorting == "a":
            unsorted_list.append(str(user_input_sorting))
            break
        elif user_input_sorting == "d":
            unsorted_list.append(str(user_input_sorting))
            break
        elif user_input_sorting == "s":
            unsorted_list.append(str(user_input_sorting))
            break
        elif user_input_sorting == "done":
            continue
        else:
            print("Invalid input, please try again")
            continue

    while user_input != "done":
        # Prompt the user for input
        user_input = input("Please enter a number, or 'done' to stop.")

        # Validate our input, and add it to out list
        # if it's a number
        try:
            # Were we given an integer?
            unsorted_list.append(int(user_input))
        except ValueError:
            try:
                # Were we given a floating-point number?
                unsorted_list.append(float(user_input))
            except ValueError:
                # Non-numeric input - if it's not "done",
                # reject it and move on
                if (user_input != "done"):
                    print ("ERROR: Non-numeric input provided.")
                continue

    # Once we get here, we're done - return the list
    return unsorted_list

def sort_list(unsorted_list):
    """Takes the unsorted list created by build_list() and
    first converts it into a JSON encoded list then
    compressed it using zlib and then sends it to a server to be sorted
    """
    # YOUR SOCKET CODE GOES HERE!
    list_json = json.dumps(unsorted_list)
    print("JSON List length", len(list_json))
    encoded_string = list_json.encode('utf-8')

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = ("localhost", 7778)
    connection.connect(addr)

    compressed = zlib.compress(encoded_string)
    connection.send(compressed)
    print("Compressed Length", len(compressed))
    print("sent", list_json)

    answer = connection.recv(4096)
    decompressed_answer = zlib.decompress(answer)
    decoded_answer = decompressed_answer.decode('utf-8')
    returned_list = json.loads(decoded_answer)

    print(returned_list)
    connection.close()
    pass

def main():
    """Call the build_list and sort_list functions, and print the result."""
    number_list = build_list()
    sort_list(number_list)

if __name__ == "__main__":
    main()

