"""
book.py

Definition of the Book model and functions to interact with book records in
the database
"""

class Book:
    """ An object representation of a Book. Each Book must have a title, author
    first name, author last name, publication year after 1900, and account_id
    of the patron that the book is checked out to (can be null).
    """

    def __init__(self, title, author_fname, author_lname, publication_year, checked_out_to):
        self._title = title
        self._author_fname = author_fname
        self._author_lname = author_lname
        self._publication_year = publication_year
        self._checked_out_to = checked_out_to


class BookDB:
    """ Manages CRUD functions for Books in the database
    """

    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor
    

    
    def select_all_books(self):
        """ Gets a list of all books in database

            Returns:
                list of dictionaries representing books: all books in the books
                table
        """

        select_all_query = """
            SELECT * from books;
        """
        self._cursor.execute(select_all_query)

        return self._cursor.fetchall()


    def select_book_by_id(self, book_id):
        """ Returns a list with the book corresponding the provided book_id

            Args:
                book_id: The book_id of the book to be selected

            Returns:
                list of a dictionary representing a book: the book record
                corresponding to the given book_id. Will be an empty list
                if no book with the provided book_id exists
        """

        select_book_by_id = """
                SELECT * from books WHERE book_id = %s;
        """
        self._cursor.execute(select_book_by_id, (book_id,))
        return self._cursor.fetchall()


    def select_all_books_by_title(self, title):
        """ Returns a list of all books with a title similar to the provided search
        term.

        Args:
            title (string): The title or keyword to search for in the title of
            a book

        Returns:
            list of dictionaries representing books: the book records
            matching the given title. Will be an empty list
            if no book matching the given title exists
        """

        select_books_by_title = """
            SELECT * from books WHERE title LIKE %s;
        """
        self._cursor.execute(select_books_by_title, (f"%{title}%",))
        return self._cursor.fetchall()


    def insert_book(self, book):
        """ Adds a new book to the books table.

        Args:
            book: The book object to be added

        Returns:
            book_id: the book_id of the newly added book record
        """

        insert_query = """
            INSERT INTO books (title, author_fname, author_lname, publication_year)
            VALUES (%s, %s, %s, %s);
        """

        self._cursor.execute(insert_query, (book._title, book._author_fname, book._author_lname, book._publication_year))
        self._cursor.execute("SELECT LAST_INSERT_ID() book_id")
        book_id = self._cursor.fetchone()
        self._db_conn.commit()

        return book_id


    def update_book(self, book_id, new_book):
        """ Sets the title, author_fname, author_lname, publication_year, and 
        checked_out_to of a given book. 

        Args:
            book_id: The book_id of the book record to be updated
            book: A book object containing the updated attributes of the book
        """

        update_query = """
            UPDATE books
            SET title=%s, 
            author_fname=%s, 
            author_lname=%s,
            publication_year=%s,
            checked_out_to=%s
            WHERE book_id=%s;
        """
        self._cursor.execute(update_query, (new_book._title, 
        new_book._author_fname, new_book._author_lname, new_book._publication_year, 
        new_book._checked_out_to, book_id))
        self._db_conn.commit()


    def delete_book_by_id(self, book_id):
        """ Deletes the book record corresponding to the given book_id

        Args:
            book_id: The book_id of the book record to be deleted
        """
        delete_query = """
            DELETE from books
            WHERE book_id=%s;
        """
        self._cursor.execute(delete_query, (book_id,))
        self._db_conn.commit()
    

    def select_available_books(self):
        """ Returns a list of all books available for checkout in database as 
        dictionaries. Available books must not be currently checked out to 
        anyone.

        Returns:
            list of dictionaries representing books: A list of all books that 
            are not currently checked out to someone.
        """

        select_available_books = """
                SELECT * from books WHERE checked_out_to is NULL;
        """
        self._cursor.execute(select_available_books)
        return self._cursor.fetchall()

    
    def select_all_books_by_patron(self, patron_id):
        """ Returns a list of all books that a given patron has currently 
        checked out

        Args:
            patron_id: The account id of a patron

        Returns:
            list of dictionaries representing books: A list of all books that 
            are checked out to the given patron
        """

        select_all_books_by_patron = """
                SELECT * from books WHERE checked_out_to = %s;
        """
        self._cursor.execute(select_all_books_by_patron, (patron_id,))
        return self._cursor.fetchall()
