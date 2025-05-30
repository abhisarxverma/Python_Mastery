from .models.book import Book, Author
from .models.loan import Loan
from .models.member import Member
from .catalog import LibraryCatalog
from .services import LoanService
from .data_import_export import *
from .analytics_engine import AnalyticsEngine
import logging

logging_file = give_absolute_path("Log/app.log")

logging.basicConfig(filename=logging_file, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_new_loan(library: "Library", loan: Loan):
    logging.info(f'Member ID {loan.member.member_id} borrowed "{loan.book.title}" | Due {loan.due_date} | Fine Paid : Rs.0')

def log_loan_return(library: "Library", loan: Loan):
    fine = library.loan_service.calculate_penalty(loan)
    logging.info(f'Member ID {loan.member.member_id} returned "{loan.book.title}" | Fine Paid Rs.{fine}')

LIBRARY_DATA_JSON_PATH = give_absolute_path("data/library.json")

class Library:

    def __init__(self, to_import: bool=True, to_save_data: bool=True):
        self.loans : dict = {}
        self.members : dict = {}
        self.catalog = LibraryCatalog()
        self.loan_service = LoanService()
        self.to_import = to_import
        self.to_save_data = to_save_data
        self.total_fine_collected = 0

        #import data from json if the program runner wants
        if to_import:
            import_authors_json(self)
            import_books_json(self)
            import_members_json(self)
            import_loans_json(self)   
     
        self.analytics_engine = AnalyticsEngine(self)

    def register_member(self, name):
        """Create a new member and add them to the library's member's set."""

        new_member = Member(name)
        self.members[new_member.member_id] = new_member
        self.loans[new_member.member_id] = {}
        if self.to_save_data: export_members_json(self)
        return new_member
    
    def find_member(self, member_id:str):
        """Finds and return the member with the given member_id if exists else return None"""

        member = self.members.get(member_id, None)
        return member
    
    def find_loan(self, member_id:str, book_title:str):
        """Finds and return the loan with the member_id and the book_title return None if not found."""

        member = self.members.get(member_id)
        if not member: raise ValueError(f"Member with Id {member_id} does not exist.")

        book = self.catalog.find_book_by_title(book_title)
        if not book: raise ValueError(f"{book_title} is not present in the library.")

        if self.loans: 
            loan = self.loans[member_id].get(book.isbn, None)
            return loan
        else: return None
    
    def find_author(self, author_id: str):
        """Finds and return the author object from the saved authors."""

        author = self.catalog.authors.get(author_id, None)
        return author
    
    def find_book(self, book_isbn: str):
        """Finds and return the book object from the books."""

        book = self.catalog.books.get(book_isbn, None)
        return book
    
    def add_new_book(self, book_title:str, author_name:str, total_copies:int=1 ):
        """Add a new book in library under the Existing author if author exists, else add new author also and then add book under them."""

        # check if the book with the same name and the same author exists
        for _, book in self.catalog.books.items():
            if book.title == book_title.lower() and book.author == author_name.lower():
                raise ValueError(f"Book with title {book_title} and Author {author_name} already exists.")

        author = self.catalog.find_author_by_name(author_name)
        
        if not author:
            new_book = Book(book_title, new_author:=Author(author_name), total_copies=total_copies)
            self.catalog.add_author(new_author)
        else:
            new_book = Book(book_title, author=author, total_copies=total_copies)

        self.catalog.add_book(new_book)
        if self.to_save_data : export_books_json(self)
        if self.to_save_data : export_authors_json(self)
        if self.to_save_data : self.catalog.total_books += 1
        if self.to_save_data : self.save_library_data()
        return new_book
    
    def loan_book(self, member_id:str, book_title:str, days:int=None):
        """Create a new loan by the member for the book for given number of days after checking if the member exist with the member_id given and the book exist in the library."""

        member = self.find_member(member_id) 
        if not member: raise ValueError(f"Member with {member_id} does not exist. Please check once again.")

        book = self.catalog.find_book_by_title(book_title)
        if not book: raise ValueError(f"{book_title} book is not present in library")

        # Book's availability check
        if book.available_copies <= 0 : raise ValueError(f"{book.title} Book is not available currently in library.")

        # Member's loan limit check
        if member.current_loans_count + 1 > member.max_loans:
            raise ValueError(f"{member.name}'s Maximum loan limit already reached.")

        new_loan = self.loan_service.create_loan(book, member, days)

        # Duplicate loan by member check
        duplicate_loan = self.find_loan(member.member_id, book.title)
        if duplicate_loan: raise ValueError(f"{member.name}'s already loaned {book.title} on {duplicate_loan.loan_date}.")

        self.loans[member.member_id][book.isbn] = new_loan
        if self.to_save_data: export_loans_json(self)

        log_new_loan(self, new_loan)

        self.analytics_engine.update_data(new_loan)

        return new_loan
    
    def return_book(self, member_id:str, book_title:str):
        """Return book, by finding the loan of the member in which the book corresponds to the book_title given."""

        loan = self.find_loan(member_id, book_title)
        if not loan: raise ValueError(f"No loan exist by Member with id {member_id} for book {book_title}")

        member = self.find_member(member_id)

        # Assuming that the member will pay the fine of the current book when he will return the book
        if fine := self.loan_service.calculate_penalty(loan):
            self.total_fine_collected += fine
            member.fine_balance -= fine

        self.loan_service.return_loan(loan)
        self.loans[member_id].pop(loan.book.isbn)
        if self.to_save_data: export_loans_json(self)
        if self.to_save_data: export_members_json(self)
        if self.to_save_data: self.save_library_data()

        print("Error in logging")
        log_loan_return(self, loan)

        return True
    
    def search_books_by_title(self, search_title:str):
        """Find the books whose title contains the search title query."""

        return [book for _, book in self.catalog.books.items() if search_title.lower() in book.title.lower()]
    
    def search_books_by_author_name(self, author_name:str):
        """Find the books whose author's name matches the given author name, return empty list if not found."""

        return [book for _, book in self.catalog.books.items() if author_name.lower() in book.author.name.lower()]
    
    def search_authors(self, search_name:str):
        """Find the authors whose name contains the search name query."""

        return [author for _, author in self.catalog.authors.items() if search_name.lower() in author.name.lower()]
    
    def get_fine(self, member_id:str):
        """Show the fine of the member by finding the member by member id."""

        member = self.find_member(member_id)
        if not member: raise ValueError(f"Invalid member id: {member_id}Please recheck.")
        fine = member.fine_balance
        return fine
    
    def get_total_books(self):
        """Returns the total books in the library catalog"""

        return self.catalog.total_books
    
    def get_currently_loaned_books(self, filter=None):
        """Returns the list of the books that are currently loaned by any member in list format, returns empty list in case of no books loaned."""

        loaned_books = []

        for member_id, loans in self.loans.items():
            for book_isbn, loan in loans.items():
                if filter == "overdue" :
                    if self.loan_service.is_overdue(loan):
                        loaned_books.append(loan)
                else:
                    loaned_books.append(loan)

        return loaned_books

    def save_library_data(self, filepath=LIBRARY_DATA_JSON_PATH):
        with open(filepath, "w") as file:
            data = {
                "Total Fine collected" : self.total_fine_collected,
                "Total Books" : self.catalog.total_books,
                "Total Members" : len(self.members),
                "Total Staff" : 10
            }
            json.dump(data, file, indent=4)

        return True
    
    def get_all_loans_of_member(self, member_id: str) -> list:
        """Finds and return all the current loans of the member with the given member id."""
        member_loans = []
        loan_dict = self.loans[member_id]
        for _, loan in loan_dict.items():
            member_loans.append(loan)

        return member_loans