import pytest

from app.models.patron import Patron

def test_patron_constructor():
    first_name = "Charlie"
    last_name = "Chaplin"
    account_type = "PROFESSOR"
    my_patron = Patron(first_name, last_name, account_type)
    assert my_patron._first_name == first_name
    assert my_patron._last_name == last_name
    assert my_patron._account_type == account_type
    

def test_patron_properties():
    first_name = "Properties"
    last_name = "Patron"
    account_type = "STAFF"
    my_patron = Patron(first_name, last_name, account_type)
    
    new_first_name = "New First Name"
    my_patron._first_name = new_first_name
    assert my_patron._first_name == new_first_name

    new_last_name = "New Last Name"
    my_patron._last_name = new_last_name
    assert my_patron._last_name == new_last_name

    new_account_type = "STUDENT"
    my_patron._account_type = new_account_type
    assert my_patron._account_type == new_account_type


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
