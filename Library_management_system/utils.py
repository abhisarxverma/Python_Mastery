# Code for some utility functions to maintain the orthogonality among models

from datetime import datetime, date, timedelta
import random
import os
import traceback

LOG_FILE_PATH = "log.txt"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def give_absolute_path(path):
    return os.path.join(BASE_DIR, path)

def date_to_str(date):
    if isinstance(date, str):  # Convert string to datetime
        date = datetime.strptime(date, "%d-%m-%Y").date()
    
    return date.strftime("%d-%m-%Y") 

def str_to_date(date: str):
    return datetime.strptime(date, "%d-%m-%Y").date()

def create_member_id(member_name):
    return "".join((str(ord(c))[-1]) for c in member_name if c.isalnum())

def compute_due_date( start: date, days : int ):
    return start + timedelta(days=days)

def create_isbn(book_title: str, author_name: str):
    """Generates a random 13-digit ISBN."""
    # prefix = "978"
    mid = "".join(str(ord(c))[1] for c in book_title) 
    core = "".join(str(ord(c))[1] for c in author_name)
    return mid+core

def create_author_id(name:str):
    pre = str(sum(ord(c) for c in name))
    core = "".join(str(ord(c))[0] for c in name)
    return pre+core

def create_loan_id(book_title:str, member_id:str):
    pre = str(sum(ord(c) for c in book_title))
    member_id_list = list(member_id)
    random.shuffle(member_id_list)
    core = "".join(member_id_list)
    return pre+core

def log_some_text(text, filepath=LOG_FILE_PATH):
    with open(filepath, "w") as file:
        file.write(text)

def raise_error(class_name: str, message: str):
    try:
        raise ValueError()
    except Exception:
        stack_trace = traceback.extract_stack()

    caller = stack_trace[-2].name
    raise ValueError(f"{class_name} : {caller} : {message}")