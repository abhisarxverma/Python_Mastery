from models import *
from services import LoanService

austin = Author("Austin Kleon")

steal_like_an_artist_book = Book("Steal like an Artis", austin, copies_available=5)

abhisar = Member("Abhisar verma", max_loans=5)

print(f"Copies available for the {steal_like_an_artist_book.title} : {steal_like_an_artist_book.copies_available}")
print()

loan_service = LoanService()

loan = loan_service.create_loan(steal_like_an_artist_book, abhisar)

print(loan)
print(f"Copies available for the {steal_like_an_artist_book.title} : {steal_like_an_artist_book.copies_available}")
print()

loan_service.return_loan(loan)

print(f"Copies available for the {steal_like_an_artist_book.title} : {steal_like_an_artist_book.copies_available}")
print()

