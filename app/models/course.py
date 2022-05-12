""" An object representation of a Course. Each Course must have a title and
a reference book.
"""
class Course:

    def __init__(self, course_title, reference_book):
        self._course_title = course_title
        self._reference_book = reference_book


""" Manages CRUD functions for Courses in the database
"""
class CourseDB:

    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor
    

    def select_all_courses(self):
        select_all_query = """
            SELECT * from courses;
        """
        self._cursor.execute(select_all_query)

        return self._cursor.fetchall()


    def select_course_by_id(self, course_id):
        select_course_by_id = """
                SELECT * from courses WHERE course_id = %s;
        """
        self._cursor.execute(select_course_by_id, (course_id,))
        return self._cursor.fetchall()


    def select_all_courses_by_title(self, course_title):
        select_courses_by_title = """
            SELECT * from courses WHERE course_title LIKE %s;
        """
        self._cursor.execute(select_courses_by_title, (f"%{course_title}%",))
        return self._cursor.fetchall()


    def insert_course(self, course):
        insert_query = """
            INSERT INTO courses (course_title, reference_book)
            VALUES (%s, %s);
        """

        self._cursor.execute(insert_query, (course._course_title, course._reference_book))
        self._cursor.execute("SELECT LAST_INSERT_ID() course_id")
        course_id = self._cursor.fetchone()
        self._db_conn.commit()
        return course_id


    def update_course(self, course_id, new_course):
        update_query = """
            UPDATE courses
            SET course_title=%s, 
            reference_book=%s
            WHERE course_id=%s;
        """
        self._cursor.execute(update_query, (new_course._course_title, 
        new_course._reference_book, course_id))
        self._db_conn.commit()


    def delete_course_by_id(self, course_id):
        delete_query = """
            DELETE from courses
            WHERE course_id=%s;
        """
        self._cursor.execute(delete_query, (course_id,))
        self._db_conn.commit()
    