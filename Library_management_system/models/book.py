from ..utils import *

class Author:
    """Represents a Author"""

    def __init__(self, name:str, biography:str=None, id:str=None):
        self.name = name
        self.biography = biography
        self.id = id or create_author_id(self.name)

    def __repr__(self):
        return f"Author({self.name!r})"
    
    def __str__(self):
        return f"Author {self.name!r}"
    
    def add_book(self, book:"Book"):
        pass

    def __hash__(self):
        return hash((self.name))
    
    def __eq__(self, other):
        return isinstance(other, Author) and self.name == other.name and self.id == other.id
    
    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "biography" : self.biography,
        }
    

class Book:
    """Represents a Book in Library"""

    def __init__(self, title, author:Author=None, isbn:str=None, total_copies:int=1, available_copies:int=None):
        self.title = title
        self.author = author
        self.isbn = isbn or create_isbn(self.title, author.name)
        self.total_copies = total_copies
        
        if total_copies < 1: raise ValueError("Total copies available in library of a book must be greater than 0.")
        
        self.available_copies = available_copies or total_copies

    def __repr__(self):
        return f"Book(Title={self.title!r} Author={self.author.name!r} ISBN={self.isbn!r} Total copies={self.total_copies!r} Copies_available={self.available_copies!r}"
    
    def __str__(self):
        return f"Book {self.title!r} by {self.author.name!r}, {self.available_copies} copies available in library."

    def __hash__(self):
        return hash((self.title, self.isbn))
    
    def __eq__(self, other:"Book"):
        return isinstance(other, Book) and self.title == other.title and self.isbn == other.isbn and self.author == other.author
    
    def serialize(self):
        return {
            "title" : self.title,
            "author" : self.author.id,
            "isbn" : self.isbn,
            "total_copies" : self.total_copies,
            "available_copies" : self.available_copies
        }
    
    