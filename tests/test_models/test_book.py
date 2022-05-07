import pytest
from datetime import datetime

from app.models.book import Book

def test_task_constructor():
    title = "My Book"
    author_fname = "Kaiya"
    author_lname = "Magnuson"
    publication_year = 2022
    checked_out_to = None
    my_book = Book(title, author_fname, author_lname, publication_year, checked_out_to)
    assert my_book._title == title
    assert my_book._author_fname == author_fname
    assert my_book._author_lname == author_lname
    assert my_book._publication_year == publication_year
    assert my_book._checked_out_to == None


# def test_task_properties():
#     desc = "Test task properties"
#     t = Task(desc)
#     assert t.description == desc
    
#     rename = "Test task description set"
#     t.description = rename
#     assert t.description == rename

#     assert t.completed == False
#     t.completed = 1
#     assert t.completed == True


# This type of testing is NOT required, but shown for example purposes
# def test_task_properties_exceptions():
#     t = Task("Foobar")

#     # Since we cannot set completed > 1 we can use pytest
#     #   to check for python errors using the following syntax.
#     with pytest.raises(ValueError):
#         t.completed = 2
    
#     # Cannot set completed < 0
#     with pytest.raises(ValueError):
#         t.completed = -1

#     # Cannot use set property on creation_datetime
#     with pytest.raises(AttributeError):
#         t.creation_datetime = datetime.now()
