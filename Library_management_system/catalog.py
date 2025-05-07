from models import *
from typing import List

class LibraryCatalog :

    def __init__(self):
        self.books = set()
        self.authors = set()

    def __repr__(self):
        return f"Books : {[book.title for book in self.books]}\nAuthors : {[author.name for author in self.authors]}"

    def add_book(self, book:Book):
        '''Add book in Library if the book is not already present.'''
        if book in self.books: raise ValueError(f"{book.title} is already in Library.")
        self.books.add(book)

    def remove_book(self, book:Book):
        '''Remove book from Library if the book is present in Library.'''
        if book not in self.books : raise ValueError(f"{book.title} is not in Library.")
        self.books.remove(book)

    def find_book_by_title(self, search_title:str) -> Book:
        '''Case insensitive book search from title, Returns None if book not found.'''
        search_book = None
        for book in self.books:
            if book.title.lower() == search_title.lower() or search_title.lower() in book.title.lower():
                search_book = book
        return search_book
    
    def add_author(self, author:Author):
        '''Add author if author's books are not already present in Library.'''
        if author in self.authors : raise ValueError(f"{author.name}'s books are already present in Library.")
        self.authors.add(author)

    def find_author_by_name(self, search_name:str) -> Author:
        '''Case insensitive author search in Library, returns None if Author does not exists.'''
        search_author = None
        for author in self.authors:
            if author.name.lower() == search_name.lower() or search_name.lower() in author.name.lower():
                search_author = author
        return search_author