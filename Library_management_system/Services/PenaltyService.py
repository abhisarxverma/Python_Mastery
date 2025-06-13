from ..models.loan import Loan
from datetime import date
from ..utils import AutoErrorDecorate

class PenaltyService(AutoErrorDecorate):

    def __init__(self):
        self.penalty_per_day = 5 # Rs 5 for one day delay
        self.total_fine_collected = 0

    def calculate_penalty(self, loan: Loan) -> float:
        if self.is_overdue(loan):
            days_late = (date.today() - loan.due_date).days
            return days_late * 5 #₹5/day
        return 0.0
    
    def is_overdue(self, loan:Loan):
        """Return True if today's date is more than the due_date of the loan, else return False."""
        
        if date.today() > loan.due_date: return True
        else : return False

    def pay_fine(self, amount: int):
        self.total_fine_collected += amount
