from .models.member import Member
from .Services import MemberService
from .Services import DataService
from .Services import CatalogService
from .Services import LoanService
from .Services import LoggingService
from .Services import PenaltyService
from .Services import AnalyticsService
from .utils import *

LIBRARY_DATA_JSON_PATH = give_absolute_path("data/library.json")

class Library:

    def __init__(self, to_import: bool=True, to_save_data: bool=True):
        self.member_service = MemberService()
        self.data_service = DataService(self)
        self.catalog_service = CatalogService()
        self.loan_service = LoanService()
        self.logging_service = LoggingService()
        self.penalty_service = PenaltyService()
        self.analytics_service = AnalyticsService()

        self.to_save_data = to_save_data
        self.to_import = to_import

    def signup_new_member(self, member_name: str):
        new_member = self.member_service.register_member(member_name)
        self.loan_service.open_loan_account(new_member.member_id)
        self.data_service.export_members_json()

    def issue_new_loan(self, member_id: str, book_name: str):
        new_loan = self.loan_service.loan_book(member_id, book_name)
        if self.to_save_data: self.data_service.export_loans_json(self)
        self.logging_service.log_new_loan(self, new_loan)
        self.analytics_service.update_data(new_loan)

    def return_loan(self, member_id:str, book_title:str, author_name:str):
        loan = self.loan_service.return_book(member_id, book_title, author_name)
        if self.to_save_data: self.data_service.export_loans_json(self)
        if self.to_save_data: self.data_service.export_members_json(self)
        if self.to_save_data: self.save_library_data()
        fine = self.penalty_service.calculate_penalty(loan)
        self.logging_service.log_loan_return(self, loan, fine)

    def get_currently_loaned_books(self, filter=None):
        """Returns the list of the books that are currently loaned by any member in list format, returns empty list in case of no books loaned."""

        loaned_books = []

        for member_id, loans in self.loan_service.pending_loans.items():
            for book_isbn, loan in loans.items():
                if filter == "overdue" :
                    if self.loan_service.is_overdue(loan):
                        loaned_books.append(loan)
                else:
                    loaned_books.append(loan)

        return loaned_books
