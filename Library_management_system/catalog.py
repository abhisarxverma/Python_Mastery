from models import *

class LibraryCatalog :

    def __init__(self):
        self.books : dict = {}
        self.authors : dict = {}
        self.total_books = 0

    def __repr__(self):
        return f"Books : {[book.title for _, book in self.books.items()]}\nAuthors : {[author.name for _, author in self.authors.items()]}"

    def add_book(self, book:Book):
        '''Add book in Library if the book is not already present.'''
        if self.books.get(book.isbn, None): raise ValueError(f"{book.title} is already in Library.")
        self.books[book.isbn] = book
        self.total_books += 1

    def remove_book(self, book:Book):
        '''Remove book from Library if the book is present in Library.'''
        if not self.books.get(book.isbn, None) : raise ValueError(f"{book.title} is not in Library.")
        del self.books[book.isbn]

    def find_book_by_title(self, search_title:str) -> Book:
        '''Case insensitive book search from title, Returns None if book not found.'''
        result_book = None
        for _, book in self.books.items():
            if book.title.lower() == search_title.lower() or search_title.lower() in book.title.lower():
                result_book = book
        return result_book
    
    def add_author(self, author:Author):
        '''Add author if author's books are not already present in Library.'''
        if self.authors.get(author.id, None): raise ValueError(f"{author.name}'s books are already present in Library.")
        self.authors[author.id] = author

    def find_author_by_name(self, search_name:str) -> Author:
        '''Case insensitive author search in Library, returns None if Author does not exists.'''
        result_author = None
        for _, author in self.authors.items():
            if author.name.lower() == search_name.lower() or search_name.lower() in author.name.lower():
                result_author = author
        return result_author