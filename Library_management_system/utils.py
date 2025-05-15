# Code for some utility functions to maintain the orthogonality among models

from datetime import datetime, date, timedelta
import random

LOG_FILE_PATH = "log.txt"

BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
RESET   = "\033[0m" 
BOLD      = "\033[1m"
UNDERLINE = "\033[4m"
BRIGHT_BLACK   = "\033[90m"
BRIGHT_RED     = "\033[91m"
BRIGHT_GREEN   = "\033[92m"
BRIGHT_YELLOW  = "\033[93m"
BRIGHT_BLUE    = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN    = "\033[96m"
BRIGHT_WHITE   = "\033[97m"

def format_date(date:datetime.date):
    return date.strftime("%d-%m-%Y")

def create_member_id(member_name):
    return "".join((str(ord(c))[-1]) for c in member_name if c.isalnum())

def compute_due_date( start: date, days : int ):
    return start + timedelta(days=days)

def create_isbn():
    """Generates a random 13-digit ISBN."""
    prefix = "978"
    core = "".join(str(random.randint(0, 9)) for _ in range(9))
    return prefix+core

def create_author_id(name:str):
    pre = str(sum(ord(c) for c in name))
    core = "".join(str(ord(c))[0] for c in name)
    return pre+core

def create_loan_id(book_title:str, member_id:str):
    pre = str(sum(ord(c) for c in book_title))
    core = "".join(random.shuffle(member_id))
    return pre+core

def log_some_text(text, filepath=LOG_FILE_PATH):
    with open(filepath, "w") as file:
        file.write(text)