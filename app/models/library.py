from api.book_api import Book, BookDB

class Library:

    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor


    """Updates a book with a new patron that its checked out to. Returns a
    list with a boolean and Book object if sucessful, error message as a string
    if failed.
    """
    def checkout_book(self, library_member_id, book_id):
        database = BookDB(self._db_conn, self._cursor)
        selected_book = database.select_book_by_id(book_id)

        if not selected_book:
            return [False, "Selected book not in database"]

        new_book = Book(selected_book[0]["title"], selected_book[0]["author_fname"], selected_book[0]["author_lname"], 
        selected_book[0]["publication_year"], library_member_id)

        database.update_book(book_id, new_book)

        new_book_representation = {"title":new_book._title, "author_fname":new_book._author_fname, "author_lname":new_book._author_lname,
        "publication_year":new_book._publication_year}

        return [True, new_book_representation]
