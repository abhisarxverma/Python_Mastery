# Code for some utility functions for the orthogonality among models

from datetime import datetime, date, timedelta
import random

def format_date(date:datetime.date):
    return date.strftime("%d-%m-%Y")

def create_member_id(member_name):
    return "".join((str(ord(c))[-1]) for c in member_name if c.isalnum())

def compute_due_date( start: date, days : int ):
    return start + timedelta(days=days)