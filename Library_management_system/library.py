from .models.member import Member
from .Services.MemberService import MemberService
from .Services.CatalogService import CatalogService
from .Services.LoanService import LoanService
from .Services.LoggingService import LoggingService
from .Services.PenaltyService import PenaltyService
from .Services.AnalyticsService import AnalyticsService
from .utils import *

LIBRARY_DATA_JSON_PATH = give_absolute_path("data/library.json")

class Library(AutoErrorDecorate):

    def __init__(self, to_import: bool=True, to_save_data: bool=True):
        self.member_service = MemberService()
        self.catalog_service = CatalogService()
        self.logging_service = LoggingService()
        self.penalty_service = PenaltyService()
        self.loan_service = LoanService(
            member_service=self.member_service,
            catalog_service=self.catalog_service,
            penalty_service=self.penalty_service
        )
        self.analytics_service = AnalyticsService(
            member_service=self.member_service,
            catalog_service=self.catalog_service,
            loan_service=self.loan_service,
            penalty_service=self.penalty_service
        )

        self.to_save_data = to_save_data
        self.to_import = to_import

        if (self.to_import) :
            self.import_members()
            self.import_library_catalog()
            self.import_loans()
            self.import_analytics_data()

    def signup_new_member(self, member_name: str):
        new_member = self.member_service.register_member(member_name)
        self.loan_service.open_loan_account(new_member.member_id)
        self.analytics_service.open_member_analytics_account(new_member)
        self.analytics_service.new_member_update()
        if self.to_save_data:
            self.export_members()
            self.export_analytics_data()
        return new_member

    def issue_new_loan(self, member_id: str, book_name: str, number_of_days: int):
        new_loan = self.loan_service.loan_book(member_id, book_name, number_of_days)
        self.logging_service.log_new_loan(new_loan)
        self.analytics_service.new_loan_update(new_loan)
        if self.to_save_data: 
            self.export_loans()
            self.export_members()
            self.export_analytics_data()
        return new_loan

    def return_loan(self, member_id:str, book_title:str, author_name:str):
        result = self.loan_service.return_book(member_id, book_title, author_name)
        self.logging_service.log_loan_return(result["loan_object"], result["fine_paid"])
        if result["fine_paid"]: self.analytics_service.update_total_fine()
        if self.to_save_data: 
            self.export_loans()
            self.export_members()
            self.export_analytics_data()
        return result["loan_object"]

    def has_no_books(self):
        return self.catalog_service.total_books == 0
    
    def get_member_fine(self, member_id: str):
        member = self.member_service.find_member(member_id)
        return member.fine_balance
    
    def add_new_book_in_catalog(self, book_title: str, book_author:str, book_copies:int):
        new_book = self.catalog_service.add_book_by_title(book_title, book_author, book_copies)
        self.analytics_service.open_book_analytics_account(new_book)
        self.analytics_service.new_book_update()
        if self.to_save_data: self.export_library_catalog()

    def search_books_by_title(self, title: str):
        return self.catalog_service.search_books_by_title(title)
    
    def search_books_by_author(self, author_name: str):
        return self.catalog_service.search_books_by_author_name(author_name)
    
    def get_total_books(self):
        return self.catalog_service.get_total_books()
    
    def get_currently_loaned_books(self, filter=None):
        return self.analytics_service.query_loaned_books(filter)
    
    def get_total_fine_collected(self):
        return self.penalty_service.total_fine_collected
    
    def get_member_details(self, member_id:str):
        return (self.member_service.find_member(member_id), self.loan_service.get_all_loans_of_member(member_id))
    
    def find_n_most_borrowed_book(self, n: int):
        return self.analytics_service.top_n_most_borrowed_books(n)

    def import_library_catalog(self):
        self.catalog_service.import_catalog()

    def export_library_catalog(self):
        self.catalog_service.export_catalog()

    def import_members(self):
        self.member_service.import_members_json()
        self.loan_service.reinitialize_loan_account_for_imported_members()
    
    def export_members(self):
        self.member_service.export_members_json()

    def import_loans(self):
        self.loan_service.import_loans_json()

    def export_loans(self):
        self.loan_service.export_loans_json()

    def export_analytics_data(self):
        self.analytics_service.export_library_stats()

    def import_analytics_data(self):
        self.analytics_service.import_library_stats()