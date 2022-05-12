"""
test_course.py

Collection of functions that test the Course model from course.py
"""

import pytest

from app.models.course import Course

def test_course_constructor():
    """ Tests the constructor for a Course object
    """

    course_title = "CS 232"
    reference_book = 1
    my_course = Course(course_title, reference_book)
    assert my_course._course_title == course_title
    assert my_course._reference_book == reference_book



def test_course_properties():
    """Tests setting the properties of a Course object
    """

    course_title = "Quantum Physics"
    reference_book = 1
    my_course = Course(course_title, reference_book)
    
    new_title = "Mediterranean Crossings"
    my_course._course_title = new_title
    assert my_course._course_title == new_title

    new_reference_book = 2
    my_course._reference_book = new_reference_book
    assert my_course._reference_book == new_reference_book
