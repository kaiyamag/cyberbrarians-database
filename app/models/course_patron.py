""" An object representation of a Course. Each Course must have a title and
a reference book.
"""
class Course_Patron:

    def __init__(self, account_id, course_id):
        self._account_id = account_id
        self._course_id = course_id


""" Manages CRUD functions for Courses in the database
"""
class Course_PatronDB:

    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor
    

    def select_all_course_patrons(self):
        select_all_query = """
            SELECT * from course_patrons;
        """
        self._cursor.execute(select_all_query)

        return self._cursor.fetchall()


    def select_course_patrons_by_account_id(self, account_id):
        select_course_patrons_by_account_id = """
                SELECT * from course_patrons WHERE account_id = %s and;
        """
        self._cursor.execute(select_course_patrons_by_account_id, (account_id))
        return self._cursor.fetchall()


    def select_course_patrons_by_course_id(self, course_id):
        select_course_patrons_by_course_id = """
                SELECT * from course_patrons WHERE course_id = %s and;
        """
        self._cursor.execute(select_course_patrons_by_course_id, (course_id))
        return self._cursor.fetchall()


    def insert_course_patron(self, course_patron):
        insert_query = """
            INSERT INTO courses (account_id, course_id)
            VALUES (%s, %s);
        """

        self._cursor.execute(insert_query, (course_patron._account_id, course_patron._course_id))
        self._db_conn.commit()
        return self._cursor.fetchone()


    def delete_course_by_course_id(self, course_id):
        delete_query = """
            DELETE from course_patrons
            WHERE course_id=%s;
        """
        self._cursor.execute(delete_query, (course_id,))
        self._db_conn.commit()
    

    def delete_course_by_account_id(self, account_id):
        delete_query = """
            DELETE from course_patrons
            WHERE account_id=%s;
        """
        self._cursor.execute(delete_query, (account_id))
        self._db_conn.commit()

    def delete_course_by_course_patron_id(self, account_id, course_id):
        delete_query = """
            DELETE from course_patrons
            WHERE course_id=%s AND account_id=%s;
        """
        self._cursor.execute(delete_query, (course_id, account_id))
        self._db_conn.commit()