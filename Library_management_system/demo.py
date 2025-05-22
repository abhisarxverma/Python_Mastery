from models import *
from services import LoanService
from library import Library
from data_import_export import *

library = Library(False, False)
print(library.catalog)

# Book 1
book1 = library.add_new_book("Show your work", "Austin Kleon", 5)
print(book1)

# Book 2
book2 = library.add_new_book("The pragmatic Programmer", "Andrew Hunt", 2)
print(book2)

# Member 1
member1 = library.register_member("Abhisar verma")
print(member1)

# Loan 1 of member 1
loan1_member1 = library.loan_book(member1.member_id, "Show your work", 3)
print(loan1_member1)

# Let's see if the book's copies available changes
print(book1)

# Loan 2 of member 1
loan2_member1 = library.loan_book(member1.member_id, "the pragmatic programmer", 10)
print(loan2_member1)

# Return of loan 1 of member 1
if library.return_book(member1.member_id, "show your work") : print("Return successful!")
else : print(f"Return failed!")

# Let's check the book copies available by searching the book by title in catalog
print(book1 := library.catalog.find_book_by_title("show your work"))

# Let's create some more books
book3 = library.add_new_book("Keep Going", "Austin Kleon")
book4 = library.add_new_book("The Maze Runner", "James Dashner")
book5 = library.add_new_book("Shadow Slave", "Guiltythree")
book6 = library.add_new_book("5 am club", "Robin Sharms")

# Let's now print Catalog
print(library.catalog)

# Now let's search books
book_search_result = library.search_books_by_title("slave")
print(book_search_result)

# Now let's find the books by author names
austin_kleon_books = library.search_books_by_author_name("kleon")
print(f"Search result for austin kleon books : {[book.author for book in austin_kleon_books]}")

# Now let's search authors
author_search_result = library.search_authors("kleon")
print(author_search_result)

stephen_king = Author("Stephen king")
it = Book("IT", stephen_king)
it_chapter2 = Book("IT-2", stephen_king)
in_a_tall_grass = Book("In a Tall Grass", stephen_king)

current_datetime = date.today()
# Subtract 2 days
two_days_before = current_datetime - timedelta(days=2)
past_loan = Loan(book3, member1, due_date=two_days_before)
library.loans[member1.member_id][book3.isbn] = past_loan
export_loans_json(library)

import logging

logging.basicConfig(filename="app.log", level=logging.INFO, format=f"[%(asctime)s - %(levelname)s - %(message)s]")

logging.info("User logged in")
logging.error("File not found: config.yaml")
