from models import *

austin = Author("Austin Kleon")

steal_like_an_artist_book = Book("Steal like an Artis", austin)

abhisar = Member("Abhisar verma", max_loans=1)

loan1 = Loan(steal_like_an_artist_book, abhisar)

print(austin)
print(steal_like_an_artist_book)
print(abhisar)
print(loan1)

loan2 = Loan(steal_like_an_artist_book, abhisar)
