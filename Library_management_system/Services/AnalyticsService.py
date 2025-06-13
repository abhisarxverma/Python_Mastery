from .MemberService import MemberService
from .CatalogService import CatalogService
from .LoanService import LoanService
from ..utils import AutoErrorDecorate

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