# Code for some utility functions to maintain the orthogonality among models

from datetime import datetime, date, timedelta
import random
import os
import traceback
import json

LOG_FILE_PATH = "log.txt"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def give_absolute_path(path):
    path = os.path.join(BASE_DIR, path)
    return path

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

# A class to auto decorate any decorator to all the subclasses
class AutoErrorDecorate:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                setattr(cls, attr_name, error_decorator(attr_value))


def error_decorator(func):
    """Decorator to capture class name, method name, and line number on error."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)  # Get full traceback
            last_trace = tb[-1]  # Get the last traceback entry (where error occurred)

            method_name = func.__name__  
            class_name = func.__qualname__.split(".")[0]  # Extract class name
            line_number = last_trace.lineno  # Extract line number

            raise ValueError(f"Error in {class_name}.{method_name} at line {line_number} - {e}")

    return wrapper

def safe_json_load(filepath: str):
    try: 
        with open(filepath, "r") as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError :
        return None
    
def safe_json_dump(data, filepath: str):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)