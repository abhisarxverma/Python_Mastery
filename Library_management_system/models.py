# Implemetation of the objects/models of the project

from typing import List, Optional
from datetime import datetime, timedelta, date
from utils import *
import random

DEFAULT_DUE_DAYS  = 10

class Author:
    """Represents a Author"""

    def __init__(self, name:str, biography:str=None, id:str=None, books:Optional[List["Book"]] = None ):
        self.name = name
        self.biography = biography
        self.books = books or set()
        self.id = id or create_author_id(self.name)

    def __repr__(self):
        return f"[Author] {self.name}"
    
    def add_book(self, book:"Book"):
        book.author = self
        self.books.add(book)

    def __hash__(self):
        return hash((self.name))
    
    def __eq__(self, other):
        return isinstance(other, Author) and self.name == other.name and self.id == other.id


class Book:
    """Represents a Book in Library"""

    def __init__(self, title, author:Author=None, isbn:str=None, copies_available:int=1 ):
        self.title = title
        self.author = author
        self.isbn = isbn or create_isbn()
        
        if copies_available < 1: raise ValueError("Copies available of a book must be greater than 0.")
        else : self.copies_available = copies_available

    def __repr__(self):
        return f"[Book] {self.title} by {self.author.name} ISBN:{self.isbn} Copies_available:{self.copies_available}"
    
    def __hash__(self):
        return hash((self.title, self.isbn))
    
    def __eq__(self, other:"Book"):
        return isinstance(other, Book) and self.title == other.title and self.isbn == other.isbn
    
class Member:
    "Represents a Member of the Library"

    def __init__(self, name, member_id=None, max_loans=5, current_loans:Optional[List["Loan"]] = None):
        self.name = name
        self.member_id = member_id or create_member_id(self.name)
        self.max_loans = max_loans
        self.current_loans = current_loans or []

    def __repr__(self):
        return f"[Member] Member_id:{self.member_id!r} Member_name:{self.name!r}"
    
    def __hash__(self):
        return hash((self.name, self.member_id))
    
    def __eq__(self, other):
        return isinstance(other, Book) and self.name == other.name and self.member_id == self.member_id
    
class Loan:
    """Represents a Book Loan issued by a Member of Library"""

    def __init__(self, book:Book, member:Member, loan_date:datetime.date=None, due_date:datetime.date=None, returned_date:datetime.date=None):
        self.book = book
        self.member = member
        self.loan_date = loan_date or date.today()
        self.due_date = due_date or compute_due_date(date.today(), DEFAULT_DUE_DAYS)
        self.returned_date = returned_date

    def __repr__(self):
        return f"[Loan] {self.member.name} for {self.book.title} on {self.loan_date.isoformat()}"