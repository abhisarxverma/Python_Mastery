import json
from ..models.book import Book, Author
from ..models.loan import Loan
from ..models.member import Member
from ..library2 import Library
from ..utils import *

LOAN_DATA_JSON_PATH = give_absolute_path("data/loans.json")
BOOKS_DATA_JSON_PATH = give_absolute_path("data/books.json")
AUTHORS_DATA_JSON_PATH = give_absolute_path("data/authors.json")
MEMBER_DATA_JSON_PATH = give_absolute_path("data/members.json")

class DataService :

    def __init__(self, library : Library):
        self.library = library

    def export_loans_json(self, filepath=LOAN_DATA_JSON_PATH):
        """Exports the existing loans data in library to json."""
        serialized_data = {member_id : {isbn : loan.serialize() for isbn, loan in loan_dict.items()} for member_id, loan_dict in self.library.loans.items()}
        with open(filepath, "w") as file:
            json.dump(serialized_data, file, indent=4)
        return True

    def import_loans_json(self, library, filepath=LOAN_DATA_JSON_PATH):
        """Imports the loans data in library from the json."""
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
        except json.decoder.JSONDecodeError :
            return False
            
        for member_id, loan_dict in data.items():
            for book_isbn, loan in loan_dict.items():
                loan = Loan.make_loan_object(library, loan)
                library.loans[member_id][book_isbn] = loan
                loan.member.fine_balance += library.loan_service.calculate_penalty(loan)
            
        self.export_members_json(library)

        return True

    def import_books_json(self, library, filepath=BOOKS_DATA_JSON_PATH):
        """Import the books data from the given json file path."""
        try:
            with open(filepath, 'r') as data_file:
                data = json.load(data_file)
        except json.decoder.JSONDecodeError:
            return False
        
        for isbn, book_dict in data.items():
            book = Book.make_book_object(book_dict)
            book.author = library.find_author(book_dict["author"])
            library.catalog.books[isbn] = book
            library.catalog.total_books += 1

        return True
        
    def export_books_json(self, library,  filepath=BOOKS_DATA_JSON_PATH):
        """Export the library books data in catalog to the json."""

        serialized_data = {isbn : book.serialize() for isbn, book in library.catalog.books.items()}

        with open(filepath, 'w') as file:
            json.dump(serialized_data, file, indent=4)

        return True

    def export_authors_json(self, library, filepath=AUTHORS_DATA_JSON_PATH):
        """Export the Authors present in library catalog to the json."""

        serialized_data = {id : author.serialize() for id, author in library.catalog.authors.items()}

        with open(filepath, "w") as file:
            json.dump(serialized_data, file, indent=4)

        return True

    def import_authors_json(self, library, filepath=AUTHORS_DATA_JSON_PATH):
        """Import the authors data from the given json filepath."""

        try:
            with open(filepath, "r") as data_file:
                data = json.load(data_file)
        except json.decoder.JSONDecodeError:
            return False
        
        for _, author_dict in data.items():
            author = Author.make_author_object(author_dict)
            library.catalog.authors[author.id] = author

        return True

    def export_members_json(self, library, filepath=MEMBER_DATA_JSON_PATH):
        """Export the members data to the json file."""

        serialized_data = {id : member.serialize() for id, member in library.members.items()}

        with open(filepath, "w") as file:
            json.dump(serialized_data, file, indent=4)

        return True

    def import_members_json(self, library, filepath=MEMBER_DATA_JSON_PATH):
        """Import the members data from the json file."""

        try:
            with open(filepath, "r") as file:
                data = json.load(file)
        except json.decoder.JSONDecodeError:
            return False
                
        for id, member_data in data.items():
            member = Member.make_member_object(member_data)
            member.fine_balance = 0
            library.members[id] = member
            library.loans[id] = {}

        return True
