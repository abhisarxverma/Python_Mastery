import json
from ..models.book import Book, Author
from ..models.loan import Loan
from ..models.member import Member
from .CatalogService import CatalogService
from .LoanService import LoanService
from .MemberService import MemberService
from .PenaltyService import PenaltyService
from .AnalyticsService import AnalyticsService
from ..utils import *

LOAN_DATA_JSON_PATH = give_absolute_path("data/loans.json")
BOOKS_DATA_JSON_PATH = give_absolute_path("data/books.json")
AUTHORS_DATA_JSON_PATH = give_absolute_path("data/authors.json")
MEMBER_DATA_JSON_PATH = give_absolute_path("data/members.json")
LIBRARY_DATA_JSON_PATH = give_absolute_path("data/library.json")
ANALYTICS_DATA_JSON_PATH = give_absolute_path("data/stats.json")

class DataService(AutoErrorDecorate) :

    def __init__(self, catalog_service:CatalogService, 
                 loan_service: LoanService,
                 member_service:MemberService, 
                 penalty_service: PenaltyService,
                 analytics_service: AnalyticsService
                 ):
        self.catalog_service = catalog_service
        self.member_service = member_service
        self.loan_service = loan_service
        self.penalty_service = penalty_service
        self.analytics_service = analytics_service

    def export_loans_json(self, filepath=LOAN_DATA_JSON_PATH):
        """Exports the existing loans data in library to json."""
        serialized_data = {member_id : {isbn : loan.serialize() for isbn, loan in loan_dict.items()} for member_id, loan_dict in self.loan_service.all_loans()}
        with open(filepath, "w") as file:
            json.dump(serialized_data, file, indent=4)
        return True

    def import_loans_json(self, filepath=LOAN_DATA_JSON_PATH):
        """Imports the loans data from the json.

        Args:
            filepath (_type_, optional): path of the json file. Defaults to LOAN_DATA_JSON_PATH.

        Returns:
            boolean: returns true if the import was successful, else raise errors for debugging.
        """
        with open(filepath, "r") as file:
            data = json.load(file)
            
        for _, loans in data.items():
            for _, loan_dict in loans.items():
                loan = Loan.make_loan_object(self.catalog_service, self.member_service, loan_dict)
                self.loan_service.add_imported_loan(loan)


        return True

    def import_books_json(self, filepath:str=BOOKS_DATA_JSON_PATH):
        """Import the books data from the given json file path."""
        with open(filepath, 'r') as data_file:
            data = json.load(data_file)

        for isbn, book_dict in data.items():
            book = Book.make_book_object(book_dict)
            self.catalog_service.add_imported_book(book, book_dict["author"])

        return True
        
    def export_books_json(self,  filepath=BOOKS_DATA_JSON_PATH):
        """Export the library books data in catalog to the json."""

        serialized_data = {isbn : book.serialize() for isbn, book in self.catalog_service.all_books()}

        with open(filepath, 'w') as file:
            json.dump(serialized_data, file, indent=4)

        return True

    def export_authors_json(self, library, filepath=AUTHORS_DATA_JSON_PATH):
        """Export the Authors present in library catalog to the json."""

        serialized_data = {id : author.serialize() for id, author in library.catalog_service.all_authors()}

        with open(filepath, "w") as file:
            json.dump(serialized_data, file, indent=4)

        return True

    def import_authors_json(self, filepath=AUTHORS_DATA_JSON_PATH):
        """Import the authors data from the given json filepath."""

        with open(filepath, "r") as data_file:
            data = json.load(data_file)

        for _, author_dict in data.items():
            author = Author.make_author_object(author_dict)
            self.catalog_service.add_author(author)

        return True

    def export_members_json(self, filepath=MEMBER_DATA_JSON_PATH):
        """Export the members data to the json file."""

        serialized_data = {id : member.serialize() for id, member in self.member_service.give_all_members()}

        with open(filepath, "w") as file:
            json.dump(serialized_data, file, indent=4)

        return True

    def import_members_json(self, filepath=MEMBER_DATA_JSON_PATH):
        """Import the members data from the json file."""

        with open(filepath, "r") as file:
            data = json.load(file)

        for _, member_data in data.items():
            member = Member.make_member_object(member_data)
            self.loan_service.open_loan_account(member.member_id)

        return True
    
    def save_library_data(self, filepath=LIBRARY_DATA_JSON_PATH):
        with open(filepath, "w") as file:
            data = {
                "Total Fine collected" : self.penalty_service.total_fine_collected,
                "Total Books" : self.catalog.total_books,
                "Total Members" : self.member_service.total_members,
                "Total Staff" : 10
            }
            json.dump(data, file, indent=4)

        return True
    
    def export_library_stats(self, filepath=ANALYTICS_DATA_JSON_PATH):
        with open(filepath, "w") as file:
            json.dump(self.analytics_service.data, file, indent=4)

        return True

    def import_library_stats(self):
        """Imports the data from the json file in the data directory"""

        with open(ANALYTICS_DATA_JSON_PATH, "r") as file:
            data = json.load(file)
        
        return data