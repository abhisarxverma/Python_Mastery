from Library_management_system import library
from ..models.book import Book, Author
from ..models.loan import Loan
from ..models.member import Member
from typing import List
from datetime import datetime, timedelta, date

BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
RESET   = "\033[0m" 
BOLD      = "\033[1m"
UNDERLINE = "\033[4m"
BRIGHT_BLACK   = "\033[90m"
BRIGHT_RED     = "\033[91m"
BRIGHT_GREEN   = "\033[92m"
BRIGHT_YELLOW  = "\033[93m"
BRIGHT_BLUE    = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN    = "\033[96m"
BRIGHT_WHITE   = "\033[97m"

BASE_COLOR = BRIGHT_CYAN
INPUT_COLOR = MAGENTA

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
7. Open Analysis Interface
8. Back to Main Menu
          """)
    
def print_analysis_interface_options():
    print(f"\n{BASE_COLOR}📊 Analysis Panel : ")
    print("""
1. Most Borrowed Books
0. Back to Admin Interface
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

def print_n_most_borrowed_books(result : list, n : int):
    print(f"\n{GREEN}Top {n} most borrowed books - \n")
    for book in result:
        print(book)
    print(f"{BASE_COLOR}")