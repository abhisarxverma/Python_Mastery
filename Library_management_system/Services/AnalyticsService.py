from .MemberService import MemberService
from .CatalogService import CatalogService
from .LoanService import LoanService
from .PenaltyService import PenaltyService
from ..utils import AutoErrorDecorate, give_absolute_path, safe_json_dump, safe_json_load
import json

ANALYTICS_DATA_JSON_PATH = give_absolute_path("data/stats.json")

class AnalyticsService(AutoErrorDecorate) :

    def __init__(self, member_service: MemberService,
                 catalog_service: CatalogService,
                 loan_service: LoanService,
                 penalty_service: PenaltyService
                 ):
        self.member_service = member_service
        self.catalog_service = catalog_service
        self.loan_service = loan_service
        self.penalty_service = penalty_service

        self.data = self.create_blank_analytics_file()
        
    def new_loan_update(self, loan):
        # print(self.data)
        self.data["Books"][loan.book.isbn]["Loan count"] += 1
        self.data["Members"][loan.member.member_id]["Loan count"] += 1
        self.export_library_stats()
        return True
    
    def new_book_update(self):
        self.data["Total Books"] = self.catalog_service.total_books

    def new_member_update(self):
        self.data["Total Members"] = self.member_service.total_members

    def update_total_fine(self):
        self.data["Total Fine Collected"] = self.penalty_service.total_fine_collected
    
    def query_loaned_books(self, filter=None):
        """Returns the list of the books that are currently loaned by any member in list format, 
        returns empty list in case of no books loaned."""

        loaned_books = []

        for _, loans in self.loan_service.give_all_loans():
            for _, loan in loans.items():
                if filter == "overdue" :
                    if self.loan_service.is_overdue(loan):
                        loaned_books.append(loan)
                else:
                    loaned_books.append(loan)

        return loaned_books
    
    def create_blank_analytics_file(self) -> dict:
        """Creates the stats file from the library's book and member's data"""
        data = {
            "Books" : {},
            "Members" : {},
            "Total Fine Collected" : self.penalty_service.total_fine_collected,
            "Total Books" : self.catalog_service.total_books,
            "Total Members" : self.member_service.total_members,
            "Total Staff" : 10
        }

        for isbn, _ in self.catalog_service.all_books():
            data["Books"][isbn] = {
                "Loan count" : 0
            }
        
        for id, _ in self.member_service.give_all_members():
            data["Members"][id] = {
                "Loan count" : 0
            }

        return data
    
    def export_library_stats(self, filepath=ANALYTICS_DATA_JSON_PATH):
        safe_json_dump(self.data, filepath)
        return True

    def import_library_stats(self, filepath=ANALYTICS_DATA_JSON_PATH):
        """Imports the data from the json file in the data directory"""

        data = safe_json_load(filepath)

        if not data: return False

        self.data = data
        
        return True
    
    def open_member_analytics_account(self, member):
        member_dict = {member.member_id : {"Loan count":0}}
        self.data["Members"].update(member_dict)
        self.export_library_stats()

    def open_book_analytics_account(self, book):
        book_dict = {book.isbn: {"Loan count": 0}}
        self.data["Books"].update(book_dict)
        self.export_library_stats()

    def top_n_most_borrowed_books(self, n : int) -> list:
        if n < 1:
            raise ValueError(f"File : {__name__} - Most borrowed book function - Number passed {n} < 1.")
        
        books_data = self.data["Books"]

        top_n_books = [t[0] for t in sorted(books_data.items(), key=lambda x: x[1]["Loan count"], reverse=True)[:n]]

        books_object_list = [self.catalog_service.find_book_by_isbn(book_isbn) for book_isbn in top_n_books]

        result = [f"{book.title} by {book.author.name}" for book in books_object_list]

        return result