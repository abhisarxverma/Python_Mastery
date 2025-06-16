from ..models.book import Book
from ..models.loan import Loan
from ..models.member import Member
from datetime import date
from .MemberService import MemberService
from .CatalogService import CatalogService
from .PenaltyService import PenaltyService
from ..utils import AutoErrorDecorate, give_absolute_path, safe_json_load, safe_json_dump
import json

LOAN_DATA_JSON_PATH = give_absolute_path("data/loans.json")

class LoanService(AutoErrorDecorate):

    def __init__(self, member_service: MemberService, catalog_service: CatalogService, penalty_service: PenaltyService):
        self.pending_loans = {}
        self.member_service = member_service
        self.catalog_service = catalog_service
        self.penalty_service = penalty_service

    def give_all_loans(self):
        return self.pending_loans.items()

    def find_loan(self, member_id:str, book_title:str = None, book_isbn:str = None) -> Loan:
        """Finds and return the loan with the member_id and the book_title return None if not found."""

        if not book_title and not book_isbn : raise ValueError ("Please provide either the book title or the book isbn to find your loan.")

        member = self.member_service.find_member(member_id)
        if not member: raise ValueError (f"Member with Id {member_id} does not exist.")

        if book_isbn:
            book = self.catalog_service.find_book_by_isbn(book_isbn)
        else:
            book = self.catalog_service.find_book_by_title(book_title)
        if not book: raise ValueError (f"{book_title} is not present in the library.")

        loan = self.pending_loans[member.member_id].get(book.isbn, None)
        return loan

        
    def loan_book(self, member_id:str, book_title:str, days:int=None):
        """Create a new loan by the member for the book for given number of days after checking if the member exist with the member_id given and the book exist in the library."""

        member = self.member_service.find_member(member_id) 
        if not member: raise ValueError(f"Member with {member_id} does not exist. Please check once again.")

        book = self.catalog_service.find_book_by_title(book_title)
        if not book: raise ValueError( f"{book_title} book is not present in library")

        # Book's availability check
        if book.available_copies <= 0 : raise ValueError(f"{book.title} Book is not available currently in library.")

        # Member's loan limit check
        if member.current_loans_count + 1 > member.max_loans:
            raise ValueError(f"{member.name}'s Maximum loan limit already reached.")

        # Duplicate loan by member check
        duplicate_loan = self.find_loan(member.member_id, book_isbn=book.isbn)
        if duplicate_loan: raise ValueError(f"{member.name}'s already loaned {book.title} on {duplicate_loan.loan_date}.")
        
        # Create new loan object
        new_loan = Loan(book, member, loan_days=days)

        # Add the loan object to the loan's dict with the right keys
        self.pending_loans[member.member_id][book.isbn] = new_loan

        # Decrement the book's available copies
        book.available_copies -= 1

        # Increase the member's current loan count
        member.current_loans_count += 1

        return new_loan
    
    def return_book(self, member_id:str, book_title:str, author_name:str):
        """Return book, by finding the loan of the member in which the book corresponds to the book_title given."""

        book = self.catalog_service.find_book_by_author_name(book_title, author_name)
        if not book: raise ValueError(f"Book with title {book_title} and author {author_name} does not exist.")

        loan = self.find_loan(member_id, book_isbn=book.isbn)
        if not loan: raise ValueError(f"No loan exist by Member with id {member_id} for book {book_title}")

        member = self.member_service.find_member(member_id)

        # Assuming that the member will pay the fine of the current book when he will return the book
        if fine := self.penalty_service.calculate_penalty(loan):
            self.penalty_service.pay_fine(fine)
            member.fine_balance -= fine

        loan.returned_date = date.today()
        loan.book.available_copies += 1
        self.pending_loans[member_id].pop(loan.book.isbn)
        
        return loan
        
    def open_loan_account(self, member_id: str):
        self.pending_loans[member_id] = {}

    def add_imported_loan(self, loan: Loan):
        self.pending_loans[loan.member.member_id][loan.book.isbn] = loan
        self.member_service.add_fine_balance(loan.member, self.penalty_service.calculate_penalty(loan))

    def get_all_loans_of_member(self, member_id: str) -> list:
        """Finds and return all the current loans of the member with the given member id."""
        member_loans = []
        loan_dict = self.pending_loans[member_id]
        for _, loan in loan_dict.items():
            member_loans.append(loan)

        return member_loans
    
    def reinitialize_loan_account_for_imported_members(self):
        for member_id, _ in self.member_service.give_all_members():
            self.open_loan_account(member_id)
    
    def export_loans_json(self, filepath=LOAN_DATA_JSON_PATH):
        """Exports the existing loans data in library to json."""
        serialized_data = {member_id : {isbn : loan.serialize() for isbn, loan in loan_dict.items()} for member_id, loan_dict in self.give_all_loans()}

        safe_json_dump(serialized_data, filepath)

        return True

    def import_loans_json(self, filepath=LOAN_DATA_JSON_PATH):
        """Imports the loans data from the json.

        Args:
            filepath (_type_, optional): path of the json file. Defaults to LOAN_DATA_JSON_PATH.

        Returns:
            boolean: returns true if the import was successful, else raise errors for debugging.
        """
        data = safe_json_load(filepath)

        if not data: return False
            
        for _, loans in data.items():
            for _, loan_dict in loans.items():
                loan = Loan.make_loan_object(self.catalog_service, self.member_service, loan_dict)
                self.add_imported_loan(loan)

        return True