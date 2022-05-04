from datetime import datetime

# Class to model Patron objects
class Patron:
    def __init__(self, first_name, last_name, account_type):
        self._first_name = first_name
        self._last_name = last_name
        self._account_type = account_type

# Class to support reading/writing patron objects with the database
class PatronDB:
    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor
    

    def select_all_patrons(self):
        select_all_query = """
            SELECT * from patrons;
        """
        self._cursor.execute(select_all_query)

        return self._cursor.fetchall()

    def select_patron_by_id(self, account_id):
        select_patron_by_id = """
                SELECT * from patrons WHERE account_id = %s;
        """
        self._cursor.execute(select_patron_by_id, (account_id,))
        return self._cursor.fetchall()


    def select_all_patrons_by_last_name(self, last_name):
        select_patrons_by_last_name = """
            SELECT * from patrons WHERE last_name LIKE %s;
        """
        self._cursor.execute(select_patrons_by_last_name, (f"%{last_name}%",))
        return self._cursor.fetchall()


    def insert_patron(self, patron):
        insert_query = """
            INSERT INTO patrons (first_name, last_name, account_type)
            VALUES (%s, %s, %s);
        """

        self._cursor.execute(insert_query, (patron.description, patron.creation_datetime, patron.completed))
        self._cursor.execute("SELECT LAST_INSERT_ID() account_id")
        account_id = self._cursor.fetchone()
        self._db_conn.commit()
        return account_id


    def delete_patron_by_id(self, account_id):
        delete_query = """
            DELETE from patrons
            WHERE id=%s;
        """
        self._cursor.execute(delete_query, (account_id,))
        self._db_conn.commit()
