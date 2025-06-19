from ..models.book import Book, Author
from ..utils import AutoErrorDecorate, give_absolute_path, safe_json_load
import json

BOOKS_DATA_JSON_PATH = give_absolute_path("data/books.json")
AUTHORS_DATA_JSON_PATH = give_absolute_path("data/authors.json")

class CatalogService(AutoErrorDecorate) :

    def __init__(self):
        self.books : dict = {}
        self.authors : dict = {}
        self.total_books = 0

    def __repr__(self):
        return f"Books : {[book.title for _, book in self.books.items()]}\nAuthors : {[author.name for _, author in self.authors.items()]}"
    
    def make_book_object(self, data):
        """Makes and return the book object from the serialized book data."""
        book = Book(
            title = data["title"],
            isbn = data["isbn"],
            total_copies = data["total_copies"],
            available_copies = data["available_copies"]
        )
        return book
    
    def make_author_object(self, data):
        """Makes and return the author object from the searialized author data."""
        author = Author(
            name=data["name"],
            id=data["id"],
            biography=data["biography"]
        )
        return author

    def all_books(self):
        return self.books.items()
    
    def all_authors(self):
        return self.authors.items()

    def add_book_by_object(self, book:Book) -> None:
        '''Add book in Library if the book is not already present.'''
        self.books[book.isbn] = book

    def remove_book(self, book:Book) -> None:
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
    
    def find_book_by_author_name(self, book_title: str, author_name: str):
        for _, book in self.books.items():
            if book.title == book_title and book.author.name == author_name:
                return book
        return None
    
    def add_book_by_title(self, book_title:str, author_name:str, total_copies:int=1 ):
        """Add a new book in library under the Existing author if author exists, else add new author also and then add book under them."""

        # check if the book with the same name and the same author exists
        for _, book in self.books.items():
            if book.title.lower() == book_title.lower() and book.author.name.lower() == author_name.lower():
                raise ValueError(f"Book with title {book_title} and Author {author_name} already exists.")

        author = self.find_author_by_name(author_name)
        
        if not author:
            new_author = Author(author_name) # Create new author
            new_book = Book(book_title, new_author, total_copies=total_copies)
            self.authors[new_author.id] = new_author
        else:
            new_book = Book(book_title, author=author, total_copies=total_copies)

        if self.find_book_by_isbn(new_book.isbn): raise ValueError(f"{new_book.title} is already in Library.")
        self.books[new_book.isbn] = new_book
        self.total_books += 1
        
        return new_book

    def search_books_by_title(self, search_title:str):
        """Find the books whose title contains the search title query."""

        return [book for _, book in self.books.items() if search_title.lower() in book.title.lower()]
    
    def search_books_by_author_name(self, author_name:str):
        """Find the books whose author's name matches the given author name, return empty list if not found."""

        return [book for _, book in self.books.items() if author_name.lower() in book.author.name.lower()]
    
    def search_authors(self, search_name:str):
        """Find the authors whose name contains the search name query."""

        return [author for _, author in self.authors.items() if search_name.lower() in author.name.lower()]
    
    def get_total_books(self):
        """Returns the total books in the library catalog"""
        return self.total_books
    
    def import_catalog(self):
        self.import_authors_json()
        self.import_books_json()

    def export_catalog(self):
        self.export_authors_json()
        self.export_books_json()

    def import_books_json(self, filepath:str=BOOKS_DATA_JSON_PATH):
        """Import the books data from the given json file path."""
        
        data = safe_json_load(filepath)
        if not data: return

        for _, book_dict in data.items():
            book = self.make_book_object(book_dict)
            book.author = self.find_author_by_id(book_dict["author"])
            self.add_book_by_object(book)
            self.total_books += 1

    def export_books_json(self,  filepath=BOOKS_DATA_JSON_PATH):
        """Export the library books data in catalog to the json."""

        serialized_data = {isbn : book.serialize() for isbn, book in self.all_books()}

        with open(filepath, 'w') as file:
            json.dump(serialized_data, file, indent=4)

    def export_authors_json(self, filepath=AUTHORS_DATA_JSON_PATH):
        """Export the Authors present in library catalog to the json."""

        serialized_data = {id : author.serialize() for id, author in self.all_authors()}

        with open(filepath, "w") as file:
            json.dump(serialized_data, file, indent=4)


    def import_authors_json(self, filepath=AUTHORS_DATA_JSON_PATH):
        """Import the authors data from the given json filepath."""

        data = safe_json_load(filepath)
        if not data: return

        for _, author_dict in data.items():
            author = self.make_author_object(author_dict)
            if self.find_author_by_id(author_dict["id"]): raise ValueError(f"{author.name}'s books are already present in Library.")
            self.authors[author.id] = author