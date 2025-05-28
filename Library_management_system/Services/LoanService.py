from ..models.book import Book
from ..models.loan import Loan
from ..models.member import Member
from datetime import date
from MemberService import MemberService
from CatalogService import CatalogService
from utils import raise_error

CLASSNAME = "LOANSERVICE"

class LoanService:

    def __init__(self, member_service: MemberService, catalog_service: CatalogService):
        self.pending_loans = {}
        self.member_service = member_service
        self.catalog_service = catalog_service

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

        try:
            loan = self.loans[member.member_id].get(book.isbn, None)
            return loan
        except Exception as e:
            raise_error(CLASSNAME, f"{e}")

        
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
        
    
    def return_loan(self, loan:Loan):
        """End the loan by removing the loan from the member's current loans and incrementing the book copies availble."""

        loan.returned_date = date.today()
        loan.book.available_copies += 1

        return True
    
    def is_overdue(self, loan:Loan):
        """Return True if today's date is more than the due_date of the loan, else return False."""
        
        if date.today() > loan.due_date: return True
        else : return False

    def calculate_penalty(self, loan: Loan) -> float:
        if self.is_overdue(loan):
            days_late = (date.today() - loan.due_date).days
            return days_late * 5 #₹5/day
        return 0.0
    
    def open_loan_account(self, member_id: str):
        self.pending_loans[member_id] = {}

    def add_imported_loan(self, loan: Loan):
        self.pending_loans[loan.member.member_id][loan.book.isbn] = loan
        self.member_service.add_fine_balance(loan.member, self.calculate_penalty(loan))