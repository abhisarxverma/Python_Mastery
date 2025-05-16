# Implemetation of the objects/models of the project

from datetime import datetime, timedelta, date
from utils import *

DEFAULT_DUE_DAYS  = 10

class Author:
    """Represents a Author"""

    def __init__(self, name:str, biography:str=None, id:str=None):
        self.name = name
        self.biography = biography
        self.id = id or create_author_id(self.name)

    def __repr__(self):
        return f"Author({self.name!r})"
    
    def __str__(self):
        return f"Author {self.name!r}"
    
    def add_book(self, book:"Book"):
        pass

    def __hash__(self):
        return hash((self.name))
    
    def __eq__(self, other):
        return isinstance(other, Author) and self.name == other.name and self.id == other.id
    
    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "biography" : self.biography,
        }
    
    @classmethod
    def make_author_object(cls, data):
        """Makes and return the author object from the searialized author data."""
        author = cls(
            name=data["name"],
            id=data["id"],
            biography=data["biography"]
        )
        return author

class Book:
    """Represents a Book in Library"""

    def __init__(self, title, author:Author=None, isbn:str=None, total_copies:int=1, available_copies:int=None):
        self.title = title
        self.author = author
        self.isbn = isbn or create_isbn()
        self.total_copies = total_copies
        
        if total_copies < 1: raise ValueError("Total copies available in library of a book must be greater than 0.")
        
        self.available_copies = available_copies or total_copies

    def __repr__(self):
        return f"Book(Title={self.title!r} Author={self.author.name!r} ISBN={self.isbn!r} Total copies={self.total_copies!r} Copies_available={self.available_copies!r}"
    
    def __str__(self):
        return f"Book {self.title!r} by {self.author.name!r}, {self.available_copies} copies available in library."

    def __hash__(self):
        return hash((self.title, self.isbn))
    
    def __eq__(self, other:"Book"):
        return isinstance(other, Book) and self.title == other.title and self.isbn == other.isbn and self.author == other.author
    
    def serialize(self):
        return {
            "title" : self.title,
            "author" : self.author.id,
            "isbn" : self.isbn,
            "total_copies" : self.total_copies,
            "available_copies" : self.available_copies
        }
    
    @classmethod
    def make_book_object(cls, data):
        """Makes and return the book object from the serialized book data."""
        book = cls(
            title = data["title"],
            isbn = data["isbn"],
            total_copies = data["total_copies"],
            available_copies = data["available_copies"]
        )
        return book
    
class Member:
    "Represents a Member of the Library"

    def __init__(self, name, member_id=None, max_loans=5, fine_balance: int=0, current_loans_count: int=0):
        self.name = name
        self.member_id = member_id or create_member_id(self.name)
        self.max_loans = max_loans
        self.fine_balance = fine_balance
        self.current_loans_count = current_loans_count

    def __repr__(self):
        return f"Member(Member_id={self.member_id!r} Member_name={self.name!r}"
    
    def __str__(self):
        return f"Member {self.name!r}"
    
    def __hash__(self):
        return hash((self.name, self.member_id))
    
    def __eq__(self, other):
        return isinstance(other, Member) and self.name == other.name and self.member_id == self.member_id
    
    def serialize(self):
        return {
            "id" : self.member_id,
            "name" : self.name,
            "fine_balance" : self.fine_balance,
            "max_loans" : self.max_loans,
            "current_loans_count" : self.current_loans_count,
        }
    
    @classmethod
    def make_member_object(cls, data:dict):
        """Makes and return the member object from the serialized member data imported from the json."""
        member = cls(
            member_id= data["id"],
            name=data["name"],
            max_loans=data["max_loans"],
            current_loans_count = data["current_loans_count"],
            fine_balance= data["fine_balance"]
        )
        return member
    
class Loan:
    """Represents a Book Loan issued by a Member of Library"""

    def __init__(self, book:Book, member:Member, loan_date:datetime.date=None, loan_days:int=None, returned_date:datetime.date=None, id: str=None):
        self.id = id or create_loan_id(book.title, member.member_id)
        self.book: Book = book
        self.member: Member = member
        self.loan_date: date = loan_date or date.today()
        self.due_date: date = date.today() + timedelta(days=loan_days) if loan_days else compute_due_date(date.today(), DEFAULT_DUE_DAYS)
        self.returned_date: date = returned_date

    def __repr__(self):
        return f"Loan(Member name={self.member.name!r} Book name={self.book.title!r} Issue date={self.loan_date.isoformat()} Due return date={self.due_date!r}"
    
    def __str__(self):
        return f"Loan by {self.member.name!r} for book {self.book.title!r} by {self.book.author.name} on {self.loan_date.isoformat()}"

    def __eq__(self, other:"Loan"):
        return isinstance(other, Loan) and self.book.isbn == other.book.isbn and self.member.member_id == other.member.member_id
    
    def serialize(self):
        return {
            "book" : self.book.isbn,
            "member_id" : self.member.member_id,
            "loan_date" : self.loan_date.isoformat(),
            "due_date" : self.due_date.isoformat(),
            "returned_date" : self.returned_date.isoformat() if self.returned_date else "N/A"
        }
    
    @classmethod
    def make_loan_object(cls, library, data, member:Member=None):
        """Makes and return the loan object from the serialized loan data."""
        loan = cls(
            book = library.find_book(data["book"]),
            member = member or library.find_member(data["member_id"]),
            loan_date = datetime.strptime(data["loan_date"], "%Y-%m-%d"),
            due_date = datetime.strptime(data["due_date"], "%Y-%m-%d"),
            returned_date = datetime.strptime(data["returned_date"], "%Y-%m-%d")
        )
        return loan
