from ..utils import *
import logging
from ..models.loan import Loan

class LoggingService:

    def __init__(self):
        self.logging_file = give_absolute_path("Log/app.log")
        logging.basicConfig(filename=self.logging_file, level=logging.INFO, format="%(asctime)s - %(message)s")

    def log_new_loan(self, loan: Loan):
        logging.info(f'Member ID {loan.member.member_id} borrowed "{loan.book.title}" | Due {loan.due_date} | Fine Paid : Rs.0')

    def log_loan_return(self, loan: Loan, fine: int):
        logging.info(f'Member ID {loan.member.member_id} returned "{loan.book.title}" | Fine Paid Rs.{fine}')
