from ..models.book import Book
from ..models.loan import Loan
from ..models.member import Member
from datetime import date
from .MemberService import MemberService
from .CatalogService import CatalogService
from .PenaltyService import PenaltyService
from ..utils import AutoErrorDecorate

class LoanService(AutoErrorDecorate):

    def __init__(self, member_service: MemberService, catalog_service: CatalogService, penalty_service: PenaltyService):
        self.pending_loans = {}
        self.member_service = member_service
        self.catalog_service = catalog_service
        self.penalty_service = penalty_service

    def all_loans(self):
        return self.pending_loans.items()

    def find_loan(self, member_id:str, book_title:str = None, book_isbn:str = None) -> Loan:
        """Finds and return the loan with the member_id and the book_title return None if not found."""

        if not book_title and not book_isbn : raise_error(CLASSNAME, "Please provide either the book title or the book isbn to find your loan.")

        member = self.member_service.find_member(member_id)
        if not member: raise_error(CLASSNAME, f"Member with Id {member_id} does not exist.")

        if book_isbn:
            book = self.catalog_service.find_book_by_isbn(book_isbn)
        else:
            book = self.catalog_service.find_book_by_title(book_title)
        if not book: raise_error(CLASSNAME, f"{book_title} is not present in the library.")

        loan = self.loans[member.member_id].get(book.isbn, None)
        return loan

        
    def loan_book(self, member_id:str, book_title:str, days:int=None):
        """Create a new loan by the member for the book for given number of days after checking if the member exist with the member_id given and the book exist in the library."""

        member = self.find_member(member_id) 
        if not member: raise_error(CLASSNAME, f"Member with {member_id} does not exist. Please check once again.")

        book = self.catalog.find_book_by_title(book_title)
        if not book: raise_error(CLASSNAME, f"{book_title} book is not present in library")

        # Book's availability check
        if book.available_copies <= 0 : raise_error(CLASSNAME, f"{book.title} Book is not available currently in library.")

        # Member's loan limit check
        if member.current_loans_count + 1 > member.max_loans:
            raise_error(CLASSNAME, f"{member.name}'s Maximum loan limit already reached.")

        # Duplicate loan by member check
        duplicate_loan = self.find_loan(member.member_id, book_isbn=book.isbn)
        if duplicate_loan: raise_error(CLASSNAME, f"{member.name}'s already loaned {book.title} on {duplicate_loan.loan_date}.")
        
        # Create new loan object
        new_loan = Loan(book, member, loan_days=days)

        # Add the loan object to the loan's dict with the right keys
        self.loans[member.member_id][book.isbn] = new_loan

        # Decrement the book's available copies
        book.available_copies -= 1

        # Increase the member's current loan count
        member.current_loans_count += 1

        return new_loan
    
    def return_book(self, member_id:str, book_title:str, author_name:str):
        """Return book, by finding the loan of the member in which the book corresponds to the book_title given."""

        book = self.catalog_service.find_book_by_author_name(book_title, author_name)
        if not book: raise_error(CLASSNAME, f"Book with title {book_title} and author {author_name} does not exist.")

        loan = self.find_loan(member_id, book_isbn=book.isbn)
        if not loan: raise_error(CLASSNAME, f"No loan exist by Member with id {member_id} for book {book_title}")

        member = self.member_service.find_member(member_id)

        # Assuming that the member will pay the fine of the current book when he will return the book
        if fine := self.penalty_service.calculate_penalty(loan):
            self.penalty_service.pay_fine(fine)
            member.fine_balance -= fine

        loan.returned_date = date.today()
        loan.book.available_copies += 1
        self.pending_loans[member_id].pop(loan.book.isbn)
        
        return True
        
    def open_loan_account(self, member_id: str):
        self.pending_loans[member_id] = {}

    def add_imported_loan(self, loan: Loan):
        self.pending_loans[loan.member.member_id][loan.book.isbn] = loan
        self.member_service.add_fine_balance(loan.member, self.calculate_penalty(loan))

    def get_all_loans_of_member(self, member_id: str) -> list:
        """Finds and return all the current loans of the member with the given member id."""
        member_loans = []
        loan_dict = self.pending_loans[member_id]
        for _, loan in loan_dict.items():
            member_loans.append(loan)

        return member_loans