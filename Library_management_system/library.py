from models import Loan, Book, Author, Member
from catalog import LibraryCatalog
from services import LoanService

from typing import Set

class Library:

    def __init__(self):
        self.members : Set[Member] = set()
        self.catalog = LibraryCatalog()
        self.loan_service = LoanService()

        #Import data from json
        data = self.catalog.import_from_json("exported_data.json")
        for book in data:
            new_book = self.add_new_book(book["title"], book["author"], total_copies=book["total_copies"])
            new_book.available_copies = book["available_copies"]
            self.catalog.books.add(new_book)

    def register_member(self, name):
        """Create a new member and add them to the library's member's set."""
        new_member = Member(name)
        self.members.add(new_member)

        return new_member
    
    def find_member(self, member_id:str):
        """Finds and return the member with the given member_id if exists else return None"""
        for member in self.members:
            if member.member_id == member_id:
                return member
        
        return None
    
    def find_loan(self, member_id:str, book_title:str):

        member = self.find_member(member_id)
        if not member: raise ValueError(f"Member with ID {member_id} does not exist.")

        loan = None
        for member_loan in member.current_loans:
            if member_loan.book.title.lower() == book_title.lower():
                loan = member_loan

        return loan
    
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
        return new_book
    
    def loan_book(self, member_id:str, book_title:str, days:int=None):
        """Create a new loan by the member for the book for given number of days after checking if the member exist with the member_id given and the book exist in the library."""

        book = self.catalog.find_book_by_title(book_title)
        if not book: raise ValueError(f"{book_title} book is not present in library")

        member = self.find_member(member_id) 
        if not member: raise ValueError(f"Member with {member_id} does not exist. Please check once again.")

        new_loan = self.loan_service.create_loan(book, member, days)

        return new_loan
    
    def return_book(self, member_id:str, book_title:str):
        """Return book, by finding the loan of the member in which the book corresponds to the book_title given."""

        loan = self.find_loan(member_id, book_title)
        if not loan: raise ValueError(f"No loan exist by Member with id {member_id} for book {book_title}")

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
    

