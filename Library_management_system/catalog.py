from models import *
from typing import List

class LibraryCatalog :

    def __init__(self):
        self.books = set()
        self.authors = set()

    def add_book(self, book:Book):
        '''Add book in Library if the book is not already present.'''
        if book in self.books: raise ValueError(f"{book.title} is already in Library.")
        self.books.add(book)

    def remove_book(self, book:Book):
        '''Remove book from Library if the book is present in Library.'''
        if book not in self.books : raise ValueError(f"{book.title} is not in Library.")
        self.books.remove(book)

    def find_books_by_title(self, title:str) -> List[Book]:
        '''Case insensitive book search from title, empty list if not matches.'''
        return [book for book in self.books if title.lower() in book.title.lower()]
    
    def add_author(self, author:Author):
        '''Add author if author's books are not already present in Library.'''
        if author in self.authors : raise ValueError(f"{author.name}'s books are already present in Library.")
        self.authors.add(author)

    def find_author_by_name(self, name:str) -> List[Author]:
        '''Case insensitive author search in Library, empty list if not matches.'''
        return [author for author in self.authors if name.lower() in author.name.lower()]