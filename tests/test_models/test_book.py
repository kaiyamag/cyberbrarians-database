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


def test_book_properties():
    title = "Properties Book"
    author_fname = "Cool"
    author_lname = "Person"
    publication_year = 2010
    checked_out_to = None
    my_book = Book(title, author_fname, author_lname, publication_year, checked_out_to)
    
    new_title = "New Title"
    my_book._title = new_title
    assert my_book._title == new_title

    new_author_fname = "Cooler"
    my_book._author_fname = new_author_fname
    assert my_book._author_fname == new_author_fname

    new_author_lname = "People"
    my_book._author_lname = new_author_lname
    assert my_book._author_lname == new_author_lname

    new_publication_year = "2050"
    my_book._publication_year = new_publication_year
    assert my_book._publication_year == new_publication_year

    assert my_book._checked_out_to == None

    


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
