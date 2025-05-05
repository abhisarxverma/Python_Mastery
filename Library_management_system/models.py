# Implemetation of the objects/models of the project

from typing import List, Optional
from datetime import datetime, timedelta, date
from utils import *
import random

DEFAULT_DUE_DAYS  = 10

class Author:
    """Represents a Author"""

    def __init__(self, name:str, biography:str=None, books:Optional[List["Book"]] = None ):
        self.name = name
        self.biography = biography
        self.books = books or []

    def __repr__(self):
        return f"[Author] {self.name}"
    
    def add_book(self, book:"Book"):
        book.author = self
        self.books.append(book)


class Book:
    """Represents a Book in Library"""

    def __init__(self, title, author:Author=None, isbn:str=None, copies_available:int=1 ):
        self.title = title
        self.author = author
        self.isbn = isbn
        
        if copies_available < 1: raise ValueError("Copies available of a book must be greater than 0.")
        else : self.copies_available = copies_available

    def __repr__(self):
        return f"[Book] {self.title} by {self.author.name} ISBN:{self.isbn} Copies_available:{self.copies_available}"
    
class Member:
    "Represents a Member of the Library"

    def __init__(self, name, member_id=None, max_loans=5, current_loans:Optional[List["Loan"]] = None):
        self.name = name
        self.member_id = member_id or create_member_id(self.name)
        self.max_loans = max_loans
        self.current_loans = current_loans or []

    def __repr__(self):
        return f"[Member] Member_id:{self.member_id!r} Member_name:{self.name!r}"
    
class Loan:
    """Represents a Book Loan issued by a Member of Library"""

    def __init__(self, book:Book, member:Member, loan_date:datetime.date=None, due_date:datetime.date=None, returned_date:datetime.date=None):
        self.book = book
        self.member = member
        self.loan_date = loan_date or date.today()
        self.due_date = due_date or compute_due_date(date.today(), DEFAULT_DUE_DAYS)
        self.returned_date = returned_date

        if len(self.member.current_loans) >= self.member.max_loans:
            raise ValueError(f"{self.member.name}'s loan limit reached.")
        
        if self.book.copies_available <= 0:
            raise ValueError(f"No copies available for {self.book.title}.")
        
        self.book.copies_available -= 1
        self.member.current_loans.append(self)

    def __repr__(self):
        return f"[Loan] {self.member.name} for {self.book.title} on {self.loan_date.isoformat()}"