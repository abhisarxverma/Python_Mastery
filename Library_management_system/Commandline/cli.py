# Command line Interface Implementation for the Library management system
from .cli_utilities import *
from  .admin_cli import admin_interface
from .member_cli import member_interface
from Library_management_system import library

cli_library = library.Library()

def main():
    welcome_message()

    while True:
        user_type = take_general_input("Are you:\n\n1. Admin\n2. Member\n3. Exit\n\nEnter here : ", color=WHITE)
        if user_type == "1" or user_type.lower() == "admin":
            admin_interface(cli_library)
        
        elif user_type == "2" or user_type.lower() == "member":
            member_interface(cli_library)

        elif user_type == "3":
            goodbye_message()
            cli_library.save_library_data()
            break

        else: 
            show_error_message("Invalid Input.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        goodbye_message()