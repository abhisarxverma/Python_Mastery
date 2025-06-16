from .MemberService import MemberService
from .CatalogService import CatalogService
from .LoanService import LoanService
from ..utils import AutoErrorDecorate, give_absolute_path, safe_json_dump, safe_json_load
import json

ANALYTICS_DATA_JSON_PATH = give_absolute_path("data/library.json")

class AnalyticsService(AutoErrorDecorate) :

    def __init__(self, member_service: MemberService,
                 catalog_service: CatalogService,
                 loan_service: LoanService
                 ):
        self.member_service = member_service
        self.catalog_service = catalog_service
        self.loan_service = loan_service

        self.data = self.create_blank_analytics_file()
        
    def update_data(self, loan):
        self.data["Books"][loan.book.isbn]["Loan count"] += 1
        self.data["Members"][loan.member.member_id]["Loan count"] += 1
        self.data_service.export_stats()
        return True
    
    def query_loaned_books(self, filter=None):
        """Returns the list of the books that are currently loaned by any member in list format, 
        returns empty list in case of no books loaned."""

        loaned_books = []

        for _, loans in self.loan_service.pending_loans.items():
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
            "Members" : {}
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
        data = {
            "Total Fine collected" : self.penalty_service.total_fine_collected,
            "Total Books" : self.catalog.total_books,
            "Total Members" : self.member_service.total_members,
            "Total Staff" : 10
        }
        safe_json_load(self.data, filepath)

        return True

    def import_library_stats(self, filepath=ANALYTICS_DATA_JSON_PATH):
        """Imports the data from the json file in the data directory"""

        data = safe_json_load(filepath)

        if not data: return False

        self.data = data
        
        return True