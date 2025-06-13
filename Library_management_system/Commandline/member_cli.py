from .cli_utilities import *

def member_interface(library) :
    while True:
        print_member_interface_options()
        
        user_choice = take_int_input(f"{YELLOW}Enter your choice> {WHITE}")

        if user_choice == 1:
            while True:
                name = get_validated_input(f"Enter Member name: ", check_minimum_length, f"{RED}\nName must be atleast 3 characters.")

                try:
                    new_member = library.signup_new_member(name)
                except Exception as e:
                    show_error_message(e)
                else:
                    show_success_message("Member successfully Registered.")
                    print(f"{BRIGHT_WHITE}Please keep your credentials.")
                    print(f"{GREEN}Member Id for {new_member.name} : {new_member.member_id}")
                    break

        elif user_choice == 2:
            while True:
                book_title = get_validated_input(f"Enter Book title: ", check_minimum_length, f"Book title must be atleast 3 characters.")

                book_author_name = get_validated_input(f"Enter Author name: ", check_minimum_length, f"Author name must be atleast 3 characters")

                try:
                    total_copies = take_int_input("Enter number of copies: ")
                except ValueError as e:
                    total_copies = None
                if total_copies and total_copies < 1:
                    show_error_message("Copies of new book cannot be negative.")
                    continue
                
                try:
                    library.add_new_book(book_title, book_author_name, total_copies)
                except Exception as e:
                    show_error_message(e)
                    break
                else:
                    show_success_message(f"Book successfully added.")
                    break

        elif user_choice == 3:
            member_id = take_general_input("Enter member id : ")
            book_name = take_general_input("Enter book name: ")
            try:
                days = int(input(f"{MAGENTA}\nEnter number of days for the loan: "))
            except ValueError as e:
                show_error_message("Please enter the number of days.")
                continue
            try:
                new_loan = library.loan_book(member_id, book_name, days)
            except Exception as e:
                show_error_message(e)
                
            else:
                show_success_message("Loan approved.")
                print(f"{BRIGHT_WHITE}You have to return on {new_loan.due_date}.")
                
            
        elif user_choice == 4:
            member_id = input(f"{MAGENTA}\nEnter member id: ")
            book_title = input(f"{MAGENTA}\nEnter book name: ")
            fine = library.find_member(member_id).fine_balance
            if fine:
                show_general_message(f"\n{YELLOW}Book returned {fine//5} day(s) late. Fine: ₹{fine}")
                show_general_message(f"{RED}You have to pay fine of: ₹{fine}")
            try:
                library.return_book(member_id, book_title)
            except Exception as e:
                show_error_message(e)                    
            else:
                show_success_message("Book returned successfully!. Thank you.")
            
            
        elif user_choice == 5:
            if not library.has_no_books():
                show_general_message("Library is Currently Empty. Sorry for the Inconvenience!")
                continue
            while True:
                print(f"{BASE_COLOR}1 - Search by Book name\n2 - Search by Author name\n")
                try:
                    selection = take_int_input("Enter search key: ")
                except ValueError as e:
                    show_error_message("Please enter valid choice.")
                    break

                if selection not in [1, 2]:
                    show_error_message("Please enter valid choice.")
                    break

                if selection == 1:
                    book_title = take_general_input(prompt="Enter book name: ")
                    result_books = library.search_books_by_title(book_title)
                    print_book_search_result(result_books) if result_books else show_general_message("No Book Found.")
                    break

                elif selection == 2:
                    author_name = take_general_input(prompt="Enter author name: ")
                    result_books = library.search_books_by_author_name(author_name)
                    print_book_search_result(result_books) if result_books else show_general_message("No Book Found.")
                    break

        # elif user_choice == 6:
        #     member_id = take_general_input(prompt="Enter Member id: ")
        #     member = library.find_member(member_id)
        #     current_fine = member.fine_balance
        #     if not current_fine:
        #         show_general_message("No Fine Balance to pay. Thank you!")
        #         continue
        #     show_general_message(f"{member.name}'s outstanding fine : {current_fine}")
        #     amount = take_int_input("Enter the amount to pay: ")
        #     try:
        #         if library.pay_fine(member_id, amount):
        #             show_general_message(f"Fine of {amount} paid successfully!\nOutstanding fine : {current_fine-amount}")
        #     except ValueError as e:
        #         show_error_message(e)

        elif user_choice == 0:
            break

        else:
            print(f"{RED}\nInvalid choice.")