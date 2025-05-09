# Command line Interface Implementation for the Library management system
from models import *
from library import Library

library = Library()

#Terminal color constants
BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
RESET   = "\033[0m" 

def check_minimum_length(string):
    if not string or len(string) < 3:
        return False
    return True

def main():
    print("Welcome to the Library Management System.\n")
    while True:
        print(f"\n{BLUE}Enter operation : \n")
        print("""1 - Register Member
2 - Add Book
3 - Loan Book
4 - Return Book
5 - Search books/author

    """)
        
        try:    
            user_choice = int(input("Enter your choice> "))
        except ValueError as e:
            print("Please enter valid choice.")
            continue

        if user_choice == 1:
            while True:
                name = input("\nEnter Member name: ")
                if not check_minimum_length(name):
                    print("Name must be atleast 3 characters.")
                    continue
                try:
                    library.register_member(name)
                except Exception as e:
                    print(f"Error occured : {e}")
                else:
                    print("Member successfully Registered.")
                    break

        elif user_choice == 2:
            while True:
                book_title = input("\nEnter Book title: ")
                if not check_minimum_length(book_title):
                    print("Book title must be atleast 3 characters.")
                    continue
                book_author_name = input("Enter Author name: ")
                if not check_minimum_length(book_author_name):
                    print("Author name must be atleast 3 characters")

                try:
                    total_copies = int(input("Enter number of copies: "))
                except ValueError as e:
                    total_copies = None
                if total_copies and total_copies < 1:
                    print("Copies of new book cannot be negative.")
                    continue
                
                try:
                    library.add_new_book(book_title, book_author_name, total_copies)
                except Exception as e:
                    print(f"Error occured : {e}")
                    continue
                else:
                    print("Book successfully added.")
                    break

        elif user_choice == 3:
            while True:
                member_id = input("Enter member id : ")
                book_name = input("Enter book name: ")
                try:
                    days = int(input("Enter number of days for the loan: "))
                except ValueError as e:
                    print("Please enter the number of days.")
                    continue
                try:
                    library.loan_book(member_id, book_name, days)
                except Exception as e:
                    print(f"Error occured : {e}")
                else:
                    print("Loan approved.")
                    break
            
        elif user_choice == 4:
            while True:
                member_id = input("Enter member id: ")
                book_title = input("Enter book name: ")

                try:
                    library.return_book(member_id, book_title)
                except Exception as e:
                    print(f"Error occured: {e}")
                else:
                    print("Book returned successfully.")
            
        elif user_choice == 5:
            while True:
                print("1 - Search by Book name\n2 - Search by Author name\n")
                try:
                    selection = int(input("Enter search key: "))
                except ValueError as e:
                    print("Please enter valid choice.")

                if selection not in [1, 2]:
                    print("Please enter valid choice.")
                    continue

                if selection == 1:
                    book_title = input("Enter book name: ")
                    result_books = library.search_books_by_title(book_title)
                    for book in result_books: print(book)
                    break

                elif selection == 2:
                    author_name = input("Enter author name: ")
                    result_books = library.search_books_by_author_name(author_name)
                    for book in result_books: print(book)
                    break

                else:
                    print("Invalid selection")

        else:
            print("Invalid choice.")

main()