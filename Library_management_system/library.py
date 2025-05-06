from models import Loan, Book, Author, Member
from catalog import LibraryCatalog
from services import LoanService

from typing import Set

class Library:

    def __init__(self):
        self.members : Set[Member] = set()
        self.catalog = LibraryCatalog()
        self.loan_service = LoanService()

    def register_member(self, name):
        """Create a new member and add them to the library's member's set."""
        new_member = Member(name)
        self.members.add(new_member)

        return new_member
    
    def add_new_book(self, book_title:str, author_name:str, copies_of_books:int=None ):
        """Add a new book in library under the Existing author if exists else add new author also and then add book under them."""

        matching_authors = self.catalog.find_author_by_name(author_name)
        
        if not matching_authors:
            new_book = Book(book_title, Author(author_name), copies_available=copies_of_books)
        else:
            author = matching_authors[0]
            new_book = Book(book_title, author=author, copies_available=copies_of_books)

        self.catalog.add_book(new_book)
        return True