"""Make 2 functions inorder to get inputs to add to a list and then sort those inputs.

Author: Yin Bo Chen
Class: CSI-275-01
Assignment: Lab 1 -- Sorting with Python

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
unsortedList = []
def build_list():
    list_input = input("Enter a number: ")
    while list_input != "Done" and list_input != "done":
        try:
            int(list_input)
            unsortedList.append(int(list_input))
            list_input = input("Enter a number: ")
        except ValueError:
            try:
                float(list_input)
                unsortedList.append(float(list_input))
                list_input = input("Enter a number: ")
            except ValueError:
                print("You must enter a number, try again:")
                list_input = input("Enter a number: ")
    print("Unsorted List: ", unsortedList)
    return unsortedList

def sort_list(unsortedList):
    unsortedList.sort()


def main():
    build_list()
    sort_list(unsortedList)
    print("")
    print("Sorted List: ", unsortedList)

if __name__ == "__main__":
    main()