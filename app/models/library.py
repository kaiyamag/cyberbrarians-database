"""
library.py

Contains the Library class
"""

from api.book_api import Book, BookDB

class Library:
    """Class for managing business logic of the application, including
    book checkout functions.
    """

    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor


    def checkout_book(self, patron_id, book_id):
        """Updates a book with a new patron that its checked out to. Only books
        that are not currently checked out to a patron can be checked out.

        Args:
            patron_id: The account_id of the patron to check the book
            out to
            book_id: The book_id of the book to be checked out.
        
        Returns:
            If checked out successfully, returns a list with the boolean True 
            and the updated book as a dictionary.
            If book was not available for checkout, returns a list with the
            boolean False and an error message as a string.
        """

        database = BookDB(self._db_conn, self._cursor)
        selected_book = database.select_book_by_id(book_id)

        if not selected_book:
            return [False, "Selected book not in database"]

        new_book = Book(selected_book[0]["title"], selected_book[0]["author_fname"], 
        selected_book[0]["author_lname"], selected_book[0]["publication_year"], patron_id)

        database.update_book(book_id, new_book)

        new_book_representation = {"title":new_book._title, "author_fname":new_book._author_fname, "author_lname":new_book._author_lname,
        "publication_year":new_book._publication_year}

        return [True, new_book_representation]