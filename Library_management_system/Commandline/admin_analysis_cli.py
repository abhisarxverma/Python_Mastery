from .cli_utilities import * 
from Library_management_system.library import Library


def analysis_interface(library:Library):
    while True:
        print_analysis_interface_options()

        command = take_general_input("Enter Command : ")

        if command == "1":
            n = take_int_input("Enter the Number of books : ")
            result = library.find_n_most_borrowed_book(n)
            print_n_most_borrowed_books(result, n)

        elif command.strip() == "0":
            break
