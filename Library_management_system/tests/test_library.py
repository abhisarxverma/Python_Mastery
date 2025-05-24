# tests/test_library.py

import pytest
from datetime import datetime, timedelta, date
from Library_management_system.models.models import *
from services import LoanService
from library import Library

@pytest.fixture
def library():
    return Library(to_import=False, to_save_data=False)

def test_add_new_books(library):
    book1 = library.add_new_book("Show your work", "Austin Kleon", 5)
    assert book1.title == "Show your work"
    assert book1.author.name == "Austin Kleon"
    assert book1.total_copies == 5
    assert book1.available_copies == 5

    book2 = library.add_new_book("The Pragmatic Programmer", "Andrew Hunt", 2)
    assert book2.title == "The Pragmatic Programmer"
    assert book2.author.name == "Andrew Hunt"
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
    assert loan.due_date == loan.loan_date + timedelta(days=3)
    assert book.available_copies == 4

def test_loan_book_insufficient_copies(library):
    book = library.add_new_book("The Pragmatic Programmer", "Andrew Hunt", 1)
    member = library.register_member("Joy Miller")
    loan = library.loan_book(member.member_id, "The Pragmatic Programmer", 10)
    member2 = library.register_member("Chirstopher zukerburg")
    with pytest.raises(ValueError) : library.loan_book(member2.member_id, "The Pragmatic Programmer", 5)
    assert book.available_copies == 0

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
    with pytest.raises(ValueError) : library.return_book(member.member_id, "5 AM Club")
    assert book.available_copies == 5

def test_search_books(library):
    library.add_new_book("Shadow Slave", "Guiltythree")
    results = library.search_books_by_title("slave")
    assert any("Shadow Slave" in book.title for book in results)

def test_search_authors(library):
    library.add_new_book("Show your work", "Austin Kleon")
    library.add_new_book("Keep Going", "Austin Kleon")
    results = library.search_books_by_author_name("kleon")
    assert all("Austin Kleon" == book.author.name for book in results)

def test_add_already_existing_book(library):
    library.add_new_book("Build Don't talk", "Raj Shamani", 3)
    with pytest.raises(ValueError) : library.add_new_book("Build Don't talk", "Raj Shamani", 3)

def test_fine_for_member(library):
    book = library.add_new_book("The Magic of Thinking Big", "Phraser McGurg", 10)
    member = library.register_member("John Doe")
    current_datetime = date.today()
    two_days_before = current_datetime - timedelta(days=2)
    past_loan = Loan(book, member, due_date=two_days_before)
    fine = library.loan_service.calculate_penalty(past_loan)
    assert fine == 10