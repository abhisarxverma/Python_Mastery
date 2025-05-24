from .cli_utilities import *

def admin_interface(library) :
    show_general_message("\nADMIN DASHBOARD\n")

    while True:
        print_admin_interface_options()
        
        admin_command = take_int_input("Enter Command : ")

        if admin_command == 1:
            total_books = library.get_total_books()
            show_general_message(f"TOTAL BOOKS IN LIBRARY : {total_books}")
            
        if admin_command == 2:
            loaned_books = library.get_currently_loaned_books()
            show_loaned_books(loaned_books)

        if admin_command == 3:
            overdue_loans = library.get_currently_loaned_books("overdue")
            show_loaned_books(overdue_loans)

        if admin_command == 4:
            total_fine_collected = library.total_fine_collected()
            show_general_message(f"Total fine Collected : Rs.{total_fine_collected}")

        if admin_command == 5:
            member_id = take_general_input("Enter Member Id : ")
            member = library.find_member(member_id)
            show_member(member)

        if admin_command == 6:
            library.save_library_data()
            show_success_message(f"Library data successfully exported.")

        if admin_command == 7:
            break