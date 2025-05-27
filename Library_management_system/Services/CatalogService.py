from ..models.book import Book, Author
from ..utils import raise_error

class CatalogService :

    def __init__(self):
        self.books : dict = {}
        self.authors : dict = {}
        self.total_books = 0

    def __repr__(self):
        return f"Books : {[book.title for _, book in self.books.items()]}\nAuthors : {[author.name for _, author in self.authors.items()]}"

    def add_book(self, book:Book) -> None:
        '''Add book in Library if the book is not already present.'''
        

    def remove_book(self, book:Book) -> None:
        '''Remove book from Library if the book is present in Library.'''
        if not self.books.get(book.isbn, None) : raise_error(CatalogService.__name__, f"{book.title} is not in Library.")
        del self.books[book.isbn]

    def find_book_by_title(self, search_title:str) -> Book:
        '''Case insensitive book search from title, Returns None if book not found.'''
        result_book = None
        for _, book in self.books.items():
            if book.title.lower() == search_title.lower() or search_title.lower() in book.title.lower():
                result_book = book
        return result_book
    
    def add_author(self, author:Author) -> None:
        '''Add author if author's books are not already present in Library.'''
        if self.authors.get(author.id, None): raise_error(CatalogService.__name__, f"{author.name}'s books are already present in Library.")
        self.authors[author.id] = author

    def find_author_by_name(self, search_name:str) -> Author:
        '''Case insensitive author search in Library, returns None if Author does not exists.'''
        result_author = None
        for _, author in self.authors.items():
            if author.name.lower() == search_name.lower() or search_name.lower() in author.name.lower():
                result_author = author
        return result_author
    
    def find_author_by_id(self, author_id: str) -> Author:
        """Finds and return the author object from the saved authors."""

        author = self.authors.get(author_id, None)
        return author
    
    def find_book_by_isbn(self, book_isbn: str) -> Author:
        """Finds and return the book object from the books."""

        book = self.books.get(book_isbn, None)
        return book
    
    def add_new_book(self, book_title:str, author_name:str, total_copies:int=1 ):
        """Add a new book in library under the Existing author if author exists, else add new author also and then add book under them."""

        # check if the book with the same name and the same author exists
        for _, book in self.books.items():
            if book.title == book_title.lower() and book.author == author_name.lower():
                raise raise_error(CatalogService.__name__, f"Book with title {book_title} and Author {author_name} already exists.")

        author = self.find_author_by_name(author_name)
        
        if not author:
            new_author = Author(author_name) # Create new author
            new_book = Book(book_title, new_author, total_copies=total_copies)
            self.add_author(new_author)
        else:
            new_book = Book(book_title, author=author, total_copies=total_copies)

        if self.books.get(book.isbn, None): raise_error(CatalogService.__name__, f"{book.title} is already in Library.")
        self.books[book.isbn] = book
        self.total_books += 1
        
        return new_book