# Module to Separate the analysis methods of the library
import json
from .utils import *

STATS_FILE_JSON_PATH = give_absolute_path("data/stats.json")

class AnalyticsEngine():

    def __init__(self, library):
        self.library = library
        self.data = self.import_stats()

    def import_stats(self):
        """Imports the data from the json file in the data directory"""
        try:
            with open(STATS_FILE_JSON_PATH, "r") as file:
                data = json.load(file)
        
        except json.decoder.JSONDecodeError:
            data = self.create_file()

        return data
    
    def export_stats(self):
        """Exports the data in to the json to save the stats."""
        with open(STATS_FILE_JSON_PATH, "w") as file:
            json.dump(self.data, file, indent=4)

        return True

    def create_file(self) -> dict:
        """Creates the stats file from the library's book and member's data"""
        data = {
            "Books" : {},
            "Members" : {}
        }

        for isbn, _ in self.library.catalog.books.items():
            data["Books"][isbn] = {
                "Loan count" : 0
            }
        
        for id, _ in self.library.members.items():
            data["Members"][id] = {
                "Loan count" : 0
            }

        with open("stats.json", "w") as file:
            with open(STATS_FILE_JSON_PATH, "w") as file:
                json.dump(data, file, indent=4)

        return data
    
    def update_data(self, loan):
        self.data["Books"][loan.book.isbn]["Loan count"] += 1
        self.data["Members"][loan.member.member_id]["Loan count"] += 1
        self.export_stats()
        return True

    def top_n_most_borrowed_books(self, n : int) -> list:
        if n < 1:
            raise ValueError(f"File : {__name__} - Most borrowed book function - Number passed {n} < 1.")
        
        books_data = self.data["Books"]

        top_n_books = [t[0] for t in sorted(books_data.items(), key=lambda x: x[1]["Loan count"], reverse=True)[:n]]

        books_object_list = [self.library.find_book(book_isbn) for book_isbn in top_n_books]

        result = [f"{book.title} by {book.author.name}" for book in books_object_list]

        return result

        