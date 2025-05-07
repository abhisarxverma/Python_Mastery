# tests/test_library.py

import pytest
from models import Book, Member
from services import LoanService
from library import Library

@pytest.fixture
def library():
    return Library()

def test_add_new_books(library):
    book1 = library.add_new_book("Show your work", "Austin Kleon", 5)
    assert book1.title == "Show your work"
    assert book1.author == "Austin Kleon"
    assert book1.total_copies == 5
    assert book1.available_copies == 5

    book2 = library.add_new_book("The Pragmatic Programmer", "Andrew Hunt", 2)
    assert book2.title == "The Pragmatic Programmer"
    assert book2.author == "Andrew Hunt"
    assert book2.total_copies == 2
    assert book2.available_copies == 2

def test_register_member(library):
    member = library.register_member("Abhisar Verma")
    assert member.name == "Abhisar Verma"
    assert isinstance(member.member_id, str)

def test_loan_book(library):
    book = library.add_new_book("Show your work", "Austin Kleon", 5)
    member = library.register_member("Abhisar Verma")
    loan = library.loan_book(member.member_id, "Show your work", 3)
    assert loan.book.title == "Show your work"
    assert loan.member.member_id == member.member_id
    assert loan.duration_days == 3
    assert book.available_copies == 2

def test_loan_book_insufficient_copies(library):
    book = library.add_new_book("The Pragmatic Programmer", "Andrew Hunt", 2)
    member = library.register_member("Abhisar Verma")
    loan = library.loan_book(member.member_id, "The Pragmatic Programmer", 10)
    assert loan is None
    assert book.available_copies == 2

def test_return_book(library):
    book = library.add_new_book("Show your work", "Austin Kleon", 5)
    member = library.register_member("Abhisar Verma")
    library.loan_book(member.member_id, "Show your work", 3)
    success = library.return_book(member.member_id, "Show your work")
    assert success is True
    assert book.available_copies == 5

def test_return_book_not_loaned(library):
    book = library.add_new_book("Show your work", "Austin Kleon", 5)
    member = library.register_member("Abhisar Verma")
    success = library.return_book(member.member_id, "Show your work")
    assert success is False
    assert book.available_copies == 5

def test_search_books(library):
    library.add_new_book("Shadow Slave", "Guiltythree")
    results = library.search_books("slave")
    assert any("Shadow Slave" in book.title for book in results)

def test_search_authors(library):
    library.add_new_book("Show your work", "Austin Kleon")
    library.add_new_book("Keep Going", "Austin Kleon")
    results = library.search_authors("kleon")
    assert all("Austin Kleon" == book.author for book in results)
