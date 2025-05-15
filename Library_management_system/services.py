from models import Loan, Book, Author, Member
from datetime import datetime, date

class LoanService:

    def create_loan(self, book:Book, member:Member, days:int=None) -> Loan:
        """Create a new loan if the member haven't exceeded the Loan limit and the book copies are available."""

        new_loan = Loan(book, member, loan_days=days)
        book.available_copies -= 1
        member.current_loans_count += 1

        return new_loan
    
    def return_loan(self, loan:Loan):
        """End the loan by removing the loan from the member's current loans and incrementing the book copies availble."""

        loan.returned_date = date.today()
        loan.book.available_copies += 1

        return True
    
    def is_overdue(self, loan:Loan):
        """Return True if today's date is more than the due_date of the loan, else return False."""
        
        if date.today() > loan.due_date: return True
        else : return False

    def calculate_penalty(self, loan: Loan) -> float:
        if self.is_overdue(loan):
            days_late = (date.today() - loan.due_date).days
            return days_late * 5 #₹5/day
        return 0.0