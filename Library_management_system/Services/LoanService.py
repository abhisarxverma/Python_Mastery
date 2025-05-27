from ..models.book import Book
from ..models.loan import Loan
from ..models.member import Member
from datetime import date
from MemberService import MemberService
from CatalogService import CatalogService
from utils import raise_error

class LoanService:

    def __init__(self, member_service: MemberService, catalog_service: CatalogService):
        self.pending_loans = {}
        self.member_service = member_service
        self.catalog_service = catalog_service

    def find_loan(self, member_id:str, book_title:str = None, book_isbn:str = None) -> Loan:
        """Finds and return the loan with the member_id and the book_title return None if not found."""

        if not book_title and not book_isbn : raise_error("find_loan", "Please provide either the book title or the book isbn to find your loan.")

        member = self.member_service.find_member(member_id)
        if not member: raise_error(self.find_loan.__name__, f"Member with Id {member_id} does not exist.")

        if book_isbn:
            book = self.catalog_service.find_book_by_isbn(book_isbn)
        else:
            book = self.catalog_service.find_book_by_title(book_title)
        if not book: raise_error(self.find_loan.__name__, f"{book_title} is not present in the library.")

        try:
            loan = self.loans[member.member_id].get(book.isbn, None)
            return loan
        except Exception as e:
            raise_error(self.find_loan.__name__, f"{e}")
        

    def create_loan(self, book:Book, member:Member, days:int=None) -> Loan:
        """Create a new loan if the member haven't exceeded the Loan limit and the book copies are available."""

        new_loan = Loan(book, member, loan_days=days)
        book.available_copies -= 1
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