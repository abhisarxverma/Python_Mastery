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

    def __init__(self, title, author:Author=None, isbn:str=None, total_copies:int=1 ):
        self.title = title
        self.author = author
        self.isbn = isbn or create_isbn()
        self.total_copies = total_copies
        
        if total_copies < 1: raise ValueError("Total copies available in library of a book must be greater than 0.")
        
        self.available_copies = total_copies

    def __repr__(self):
        return f"\n[Book] \nTitle: {self.title} \nAuthor: {self.author.name} \nISBN: {self.isbn} \nTotal copies : {self.total_copies} \nCopies_available:{self.available_copies}"
    
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
        return f"\n[Member] \nMember_id:{self.member_id!r} \nMember_name:{self.name!r}"
    
    def __hash__(self):
        return hash((self.name, self.member_id))
    
    def __eq__(self, other):
        return isinstance(other, Book) and self.name == other.name and self.member_id == self.member_id
    
class Loan:
    """Represents a Book Loan issued by a Member of Library"""

    def __init__(self, book:Book, member:Member, loan_date:datetime.date=None, loan_days:int=None, returned_date:datetime.date=None):
        self.book = book
        self.member = member
        self.loan_date = loan_date or date.today()
        self.due_date = date.today() + timedelta(days=loan_days) if loan_days else compute_due_date(date.today(), DEFAULT_DUE_DAYS)
        self.returned_date = returned_date

    def __repr__(self):
        return f"\n[Loan] \nMember name : {self.member.name} \nBook name : {self.book.title} \nIssue date : {self.loan_date.isoformat()} \nDue return date : {self.due_date}"
    
    def __eq__(self, other:"Loan"):
        return isinstance(other, Loan) and self.book.isbn == other.book.isbn and self.member.member_id == other.member.member_id