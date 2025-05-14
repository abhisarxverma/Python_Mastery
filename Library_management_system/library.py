from models import Loan, Book, Author, Member
from catalog import LibraryCatalog
from services import LoanService
from utils import *
import json

from typing import Set, Dict

MEMBER_DATA_JSON_PATH = "data/members.json"
LOAN_DATA_JSON_PATH = "data/loans.json"
BOOKS_DATA_JSON_PATH = "data/books.json"
AUTHORS_DATA_JSON_PATH = "data/authors.json"

class Library:

    def __init__(self):
        self.loans : dict = {}
        self.members : dict = {}
        self.catalog = LibraryCatalog()
        self.loan_service = LoanService()

        #import books from json
        books = self.catalog.import_books_from_json()
        for book in books:
            new_book = self.add_new_book(book["title"], book["author"], total_copies=book["total_copies"])
            new_book.available_copies = book["available_copies"]
            self.catalog.books.add(new_book)

        #import members from json
        self.import_members_json()

        #import loans from json
        self.import_loans_json()

    def register_member(self, name):
        """Create a new member and add them to the library's member's set."""
        new_member = Member(name)
        self.members[new_member.member_id] = new_member
        self.loans[new_member.member_id] = []
        self.export_members_json()
        return new_member
    
    def find_member(self, member_id:str):
        """Finds and return the member with the given member_id if exists else return None"""
        member = self.members.get(member_id, None)
        return member
    
    def find_loan(self, member_id:str, book_title:str):
        """Finds and return the loan with the member_id and the book_title return None if not found."""
        member = self.members.get(member_id)
        if not member: raise ValueError(f"Member with Id {member.member_id} does not exist.")

        loan = self.loans[member_id].get(book_title, None)
        return loan
    
    def find_author(self, author_id: str):
        """Finds and return the author object from the saved authors."""
        author = self.catalog.authors.get(author_id, None)
        return author
    
    def add_new_book(self, book_title:str, author_name:str, total_copies:int=1 ):
        """Add a new book in library under the Existing author if author exists, else add new author also and then add book under them."""

        # check if the book with the same name and the same author exists
        for book in self.catalog.books:
            if book.title == book_title and book.author.name == author_name:
                raise ValueError(f"Book with title {book_title} and Author {author_name} already exists.")

        author = self.catalog.find_author_by_name(author_name)
        
        if not author:
            new_book = Book(book_title, new_author:=Author(author_name), total_copies=total_copies)
            self.catalog.authors.add(new_author)
        else:
            new_book = Book(book_title, author=author, total_copies=total_copies)

        self.catalog.add_book(new_book)
        self.catalog.export_books_json()
        return new_book
    
    def loan_book(self, member_id:str, book_title:str, days:int=None):
        """Create a new loan by the member for the book for given number of days after checking if the member exist with the member_id given and the book exist in the library."""

        book = self.catalog.find_book_by_title(book_title)
        if not book: raise ValueError(f"{book_title} book is not present in library")

        member = self.find_member(member_id) 
        if not member: raise ValueError(f"Member with {member_id} does not exist. Please check once again.")

        # Book's availability check
        if book.available_copies <= 0 : raise ValueError(f"{book.title} Book is not available currently in library.")

        # Member's loan limit check
        if member.current_loans_count + 1 > member.max_loans:
            raise ValueError(f"{member.name}'s Maximum loan limit already reached.")

        new_loan = self.loan_service.create_loan(book, member, days)

        # Duplicate loan by member check
        duplicate_loan = self.find_loan(member.member_id, book.title)
        if duplicate_loan: raise ValueError(f"{member.name}'s already loaned {book.title} on {duplicate_loan.loan_date}.")

        self.loans[member.member_id][book.isbn] = new_loan
        self.export_loans_json()
        return new_loan
    
    def return_book(self, member_id:str, book_title:str):
        """Return book, by finding the loan of the member in which the book corresponds to the book_title given."""

        loan = self.find_loan(member_id, book_title)
        if not loan: raise ValueError(f"No loan exist by Member with id {member_id} for book {book_title}")

        if fine := self.loan_service.calculate_penalty(loan):
            loan.member.fine_balance += fine

        self.loan_service.return_loan(loan)
        return True
    
    def search_books_by_title(self, search_title:str):
        """Find the books whose title contains the search title query."""
        return [book for book in self.catalog.books if search_title.lower() in book.title.lower()]
    
    def search_books_by_author_name(self, author_name:str):
        """Find the books whose author's name matches the given author name, return empty list if not found."""
        return [book for book in self.catalog.books if author_name.lower() in book.author.name.lower()]
    
    def search_authors(self, search_name:str):
        """Find the authors whose name contains the search name query."""
        return [author for author in self.catalog.authors if search_name.lower() in author.name.lower()]
    
    def get_fine(self, member_id:str):
        """Show the fine of the member by finding the member by member id."""
        member = self.find_member(member_id)
        if not member: raise ValueError(f"Invalid member id: {member_id}Please recheck.")
        fine = member.fine_balance
        return fine
    
    def pay_fine(self, member_id:str, amount: int):
        """Pay Fine by finding the member by member id and subtracting the amount paid from the member's fine balance."""
        member = self.find_member(member_id)
        if not member: raise ValueError(f"Invalid Member id : {member_id}. Please recheck.")
        member.fine_balance -= amount
        return True

    def export_members_json(self, filepath=MEMBER_DATA_JSON_PATH):
        """Export the members data to the json file."""
        serialized_data = {id : member.serialize() for id, member in self.members.items()}
        with open(filepath, "w") as file:
            json.dump(serialized_data, file, indent=4)
        return True

    def import_members_json(self, filepath=MEMBER_DATA_JSON_PATH):
        """Import the members data from the json file."""
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
        except json.decoder.JSONDecodeError:
            return False
        
        for id, member_data in data.items():
            member = self.make_member_object(member_data)
            self.members[id] = member
            self.loans[id] = []

        return True

    def make_member_object(self, data:dict):
        """Makes and return the member object from the serialized member data imported from the json."""
        member = Member(
            member_id= data["id"],
            name=data["name"],
            max_loans=data["max_loans"],
            current_loans_count = data["current_loans_count"],
            fine_balance= data["fine_balance"]
        )
        return member

    def make_loan_object(self, data, member:Member=None):
        """Makes and return the loan object from the serialized loan data."""
        loan = Loan(
            book = self.catalog.find_book_by_title(data["book"]),
            member = member or self.find_member(data["member_id"]),
            loan_date = datetime.strptime(data["loan_date"], "%Y-%m-%d"),
            due_date = datetime.strptime(data["due_date"], "%Y-%m-%d"),
            returned_date = datetime.strptime(data["returned_date"], "%Y-%m-%d")
        )
        return loan
    
    def make_book_object(self, data):
        """Makes and return the book object from the serialized book data."""
        book = Book(
            title = data["title"],
            author = None
        )

    def make_author_object(self, data):
        """Makes and return the author object from the searialized author data."""
        author = Author(
            name=data["name"],
            id=data["id"],
            biography=data["biography"]
        )
    
    def export_loans_json(self, filepath=LOAN_DATA_JSON_PATH):
        """Exports the existing loans data in library to json."""
        serialized_data = {member_id : {isbn : loan.serialize() for isbn, loan in loan_dict.items()} for member_id, loan_dict in self.loans.items()}
        with open(filepath, "w") as file:
            json.dump(serialized_data, file)
        return True
    
    def import_loans_json(self, filepath=LOAN_DATA_JSON_PATH):
        """Imports the loans data in library from the json."""
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
        except json.decoder.JSONDecodeError :
            return False
        
        for member_id, loan_dict in data.items():
            for book_isbn, loan in loan_dict.items():
                self.loans[member_id][book_isbn] = self.make_loan_object(loan)

        return True
    
    def import_books_from_json(self, filepath=BOOKS_DATA_JSON_PATH):
        """Import the books data from the given json file path."""
        try:
            with open(filepath, 'r') as data_file:
                data = json.load(data_file)
        except json.decoder.JSONDecodeError:
            return False
        
    def export_books_to_json(self, filepath=BOOKS_DATA_JSON_PATH):
        """Export the library books data in catalog to the json."""
        serialized_data = [book.serialize() for book in self.books]
        with open(filepath, 'w') as file:
            json.dump(serialized_data, file, indent=4)
        return True
    
    def export_authors_json(self, filepath=AUTHORS_DATA_JSON_PATH):
        """Export the Authors present in library catalog to the json."""
        serialized_data = {id : author.serialize() for id, author in self.catalog.authors.items()}
        with open(filepath, "w") as file:
            json.dump(serialized_data, file, indent=4)
        return True
    
    def import_authors_from_json(self, filepath=AUTHORS_DATA_JSON_PATH):
        """Import the authors data from the given json filepath."""
        try:
            with open(filepath, "r") as data_file:
                data = json.load(data_file)
        except json.decoder.JSONDecodeError:
            return None
        
        for id, author_dict in data.items():
            author = Author()