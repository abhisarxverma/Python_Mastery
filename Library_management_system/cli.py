# Command line Interface Implementation for the Library management system
from library import Library
from utils import *
from models import *
from typing import List

BASE_COLOR = BRIGHT_CYAN
INPUT_COLOR = MAGENTA

library = Library()

def check_minimum_length(string):
    if not string or len(string) < 3:
        return False
    return True

def get_validated_input(prompt, validation_fn, error_message):
    while True:
        value = input(f"{INPUT_COLOR}\n{prompt}{WHITE}")
        if validation_fn(value):
            return value
        print(f"{RED}\n{error_message}{WHITE}")

def show_success_message(message):
    print(f"{GREEN}\n{message}{WHITE}")

def show_error_message(message):
    print(f"{RED}\n{message}{WHITE}")

def take_general_input(prompt, color=None):
    user_input = input(f"{color or INPUT_COLOR}\n{prompt}{WHITE}")
    return user_input

def print_book_search_result(result):
    print(f"{BRIGHT_GREEN}\n", end="")
    for book in result: print(book)

def show_general_message(message):
    print(f"{BRIGHT_WHITE}\n{message}{WHITE}")

def take_int_input(message):
    try:
        user_input = int(input(f"\n{INPUT_COLOR}{message}{WHITE}"))
        return user_input
    except ValueError as e:
        return None

def welcome_message():
    print(f"{BASE_COLOR}Welcome to the Library Management System.\n")

def goodbye_message():
    print(f"Thank you for using the system. Good bye, take care!😄")
    print("Shutting down....")

def print_member_interface_options():
    print(f"\n{BASE_COLOR}📚 Member Interface : \n")
    print("""1 - Register Member
2 - Add Book
3 - Loan Book
4 - Return Book
5 - Search books/author
(0 - Exit)

    """)

def print_admin_interface_options():
    print(f"\n{BASE_COLOR}🛠️ Admin Panel :")
    print("""
1. View total number of books
2. View currently loaned books
3. View overdue books and defaulters
4. View total fine collected
5. Search Member by ID
6. Export Library Report (Optional)
7. Back to Main Menu
          """)
    
def print_loan_summary(loan: Loan):

    due_days = 0
    if date.today() > loan.due_date:
        due_days = (date.today() - loan.due_date).days

    print(f"""{loan.book.title}"
Borrowed by : {loan.member.member_id} ({loan.member.name})
Borrowed on : {loan.loan_date}
Due Date    : {loan.due_date}
Status      : {f"{RED}❗ Overdue by {due_days} days{YELLOW} | Penalty = Rs.{library.loan_service.calculate_penalty(loan)}" if due_days!=0 else f"{GREEN}⏳ On Time{YELLOW}"}
    """)

def show_loaned_books(loans : List[Loan]):
    if not loans:
        show_general_message("No Loans currently pending.")
        return

    total_loans = len(loans)

    print(f"\n{YELLOW}Currently Loaned Books (Total : {total_loans})\n")

    for number, loan in enumerate(loans, start=1):
        print(f"{number}.", end="")
        print_loan_summary(loan)
        print("-"*50)

def show_member(member: Member):
    print(f"""
Id   : {member.member_id}
Name : {member.name}
Max loans limit : {member.max_loans}
Current loans count : {member.current_loans_count}
          """)
    
    loans = library.get_all_loans_of_member(member.member_id)
    show_loaned_books(loans)

          
def member_interface():
    while True:
        print_member_interface_options()
        
        user_choice = take_int_input(f"{YELLOW}Enter your choice> {WHITE}")

        if user_choice == 1:
            while True:
                name = get_validated_input(f"Enter Member name: ", check_minimum_length, f"{RED}\nName must be atleast 3 characters.")

                try:
                    new_member = library.register_member(name)
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
            if not library.get_total_books():
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

def admin_interface() :
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


def main():
    welcome_message()

    while True:
        user_type = take_general_input("Are you:\n\n1. Admin\n2. Member\n3. Exit\n\nEnter here : ", color=WHITE)
        if user_type == "1" or user_type.lower() == "admin":
            admin_interface()
        
        elif user_type == "2" or user_type.lower() == "member":
            member_interface()

        elif user_type == "3":
            goodbye_message()
            break

        else: 
            show_error_message("Invalid Input.")


if __name__ == "__main__":
    main()