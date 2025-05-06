from models import Loan, Book, Author, Member
from datetime import datetime, date

class LoanService:

    def create_loan(self, book:Book, member:Member) -> Loan:
        """Create a new loan if the member haven't exceeded the Loan limit and the book copies are available."""

        # Member's Loan count check
        if len(member.current_loans) >= member.max_loans: raise ValueError(f"{member.name}'s loan count is already full.")

        # Book's availability check
        if book.copies_available <= 0 : raise ValueError(f"{book.title} Book is not available currently in library.")

        new_loan = Loan(book, member)

        member.current_loans.append(new_loan)
        
        book.copies_available -= 1

        return new_loan
    
    def return_loan(self, loan:Loan):
        """End the loan by removing the loan from the member's current loans and incrementing the book copies availble."""

        if loan not in loan.member.current_loans:
            raise ValueError(f"Loan record not found for member {loan.member.name} for book {loan.book.title}.")

        loan.returned_date = date.today()
        loan.book.copies_available += 1
        loan.member.current_loans.remove(loan)

        return True