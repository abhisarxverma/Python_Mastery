from ..utils import *
from .book import Book, Author
from .member import Member

from datetime import datetime, timedelta, date

DEFAULT_DUE_DAYS  = 10

class Loan:
    """Represents a Book Loan issued by a Member of Library"""

    def __init__(self, book:Book, member:Member, loan_date:datetime.date=None, due_date:datetime.date=None, loan_days:int=None, returned_date:datetime.date=None, id: str=None):
        self.id = id or create_loan_id(book.title, member.member_id)
        self.book: Book = book
        self.member: Member = member
        self.loan_date: date = loan_date or date.today()
        self.due_date: date = due_date or (date.today() + timedelta(days=loan_days) if loan_days else compute_due_date(date.today(), DEFAULT_DUE_DAYS))
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
            "loan_date" : date_to_str(self.loan_date),
            "due_date" : date_to_str(self.due_date),
            "returned_date" : date_to_str(self.returned_date) if isinstance(self.returned_date, date) else "N/A"
        }
    
    @classmethod
    def make_loan_object(cls, library, data, member:Member=None):
        """Makes and return the loan object from the serialized loan data."""
        loan = cls(
            book = library.find_book(data["book"]),
            member = member or library.find_member(data["member_id"]),
            loan_date = str_to_date(data["loan_date"]),
            due_date = str_to_date(data["due_date"]),
            returned_date = str_to_date(data["returned_date"]) if data["returned_date"] != "N/A" else "N/A"
        )
        return loan
