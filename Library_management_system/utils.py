# Code for some utility functions for the orthogonality among models

from datetime import datetime, date, timedelta
import random

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