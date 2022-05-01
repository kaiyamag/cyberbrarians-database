""" An object representation of a Book. Each Book must have a title, author
first name, author last name, and publication year after 1900.
"""
class Book:

    def __init__(self, title, author_fname, author_lname, publication_year):
        self._title = title
        self._author_fname = author_fname
        self._author_lname = author_lname
        self._publication_year = publication_year


""" Manages CRUD functions for Books in the database
"""
class BookDB:

    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor
    

    def select_all_books(self):
        select_all_query = """
            SELECT * from books;
        """
        self._cursor.execute(select_all_query)

        return self._cursor.fetchall()


    def select_book_by_id(self, book_id):
        select_book_by_id = """
                SELECT * from book WHERE book_id = %s;
        """
        self._cursor.execute(select_book_by_id, (book_id,))
        return self._cursor.fetchall()


    def select_all_books_by_title(self, title):
        select_books_by_title = """
            SELECT * from books WHERE title LIKE %s;
        """
        self._cursor.execute(select_books_by_title, (f"%{title}%",))
        return self._cursor.fetchall()


    def insert_book(self, book):
        insert_query = """
            INSERT INTO books (title, author_fname, author_lname, publication_year)
            VALUES (%s, %s, %s, %s);
        """

        self._cursor.execute(insert_query, (book._title, book._author_fname, book._author_lname, book._publication_year))
        self._cursor.execute("SELECT LAST_INSERT_ID() book_id")
        book_id = self._cursor.fetchone()
        self._db_conn.commit()
        return book_id


    # def update_task(self, task_id, new_task):
    #     update_query = """
    #         UPDATE tasks
    #         SET description=%s
    #         WHERE id=%s;
    #     """
    #     self._cursor.execute(update_query, (new_task.description, task_id))
    #     self._db_conn.commit()

    def delete_book_by_id(self, book_id):
        delete_query = """
            DELETE from books
            WHERE book_id=%s;
        """
        self._cursor.execute(delete_query, (book_id,))
        self._db_conn.commit()
