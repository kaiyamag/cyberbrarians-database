"""
test_book_api.py

Collection of functions to be run with pytest to test all api functionality
"""

import json


# By using the parameter flask_test_client, we automatically get access to a "fake" version
#   of our webservice application to test our api. This is provided by the pytest fixture in conftest.py
#   (note the parameter name matches the name of the fixture function).
def test_posting_a_book(flask_test_client):
    """Test adding multiple books to the database via POST request
    Args:
        flask_test_client: fixture function from conftest.py
    """

    # Simulate a post request that sends json data
    request = flask_test_client.post('api/v1/books/', json={'title': 'My Favorite Book', 
    'author_fname': 'Nobody', 'author_lname': 'In particular', 'publication_year': 1999,
    'checked_out_to': None})

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # The body of the response is JSON, so we turn it from a string into a JSON
    #   object. The json object can be treated similarly to a dictionary or list
    #   based on the format of the JSON content.
    data = json.loads(request.data.decode())

    assert data['status'] == "success"
    assert data['book_id'] == 1

    request = flask_test_client.post('api/v1/books/', json={'title': 'A Second Book', 
    'author_fname': 'King George', 'author_lname': 'II', 'publication_year': 1901,
    'checked_out_to': None})

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    assert data['book_id'] == 2


def test_get_all_books(flask_test_client):
    """Test getting a list of all books in database. Relies on book records
    added in test_posting_a_book().

    Args:
        flask_test_client: fixture function from conftest.py
    """
    
    # Here is how to use the test client to simulate a GET request
    request = flask_test_client.get('/api/v1/books/')

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # Verify data
    assert len(data['books']) == 2

    # When getting all the tasks, we cannot rely on the ordering because I did
    #   not enforce an ordering on the SQL query. Always be careful with
    #   assumptions about order unless you have explicity
    #   ensured that the content will be ordered
    for books in data['books']:
        if books['book_id'] == 1:
            assert books['title'] == 'My Favorite Book'
            assert books['author_fname'] == 'Nobody'
            assert books['author_lname'] == 'In particular'
            assert books['publication_year'] == 1999
            assert books['checked_out_to'] == None
        elif books['book_id'] == 2:
            assert books['title'] == 'A Second Book'
            assert books['author_fname'] == 'King George'
            assert books['author_lname'] == 'II'
            assert books['publication_year'] == 1901
            assert books['checked_out_to'] == None
        else:
            # We should not get here as there are only two items inserted
            raise Exception("Unknown book found in database!")


def test_get_book_by_id(flask_test_client):
    """Test selecting a book from the database by its book_id vie GET
    Args:
        flask_test_client: fixture function from conftest.py
    """
    
    # Here is how to use the test client to simulate a GET request
    request = flask_test_client.get('/api/v1/books/1/')

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    # Make sure we got a status code of 200
    assert request.status_code == 200

    assert len(data['books']) == 1

    # Get the first item from the list of tasks (which should only be task id 1)
    book = data['books'][0]

    # Check the id and description
    assert book['book_id'] == 1
    assert book['title'] == 'My Favorite Book'
    assert book['author_fname'] == 'Nobody'
    assert book['author_lname'] == 'In particular'
    assert book['publication_year'] == 1999
    assert book['checked_out_to'] == None


def test_get_book_by_title_search(flask_test_client):
    """Test selecting a book by a keyword search in its title via GET
    Args:
        flask_test_client: fixture function from conftest.py
    """

    # Here is how to use the test client to simulate a GET request with a query string
    request = flask_test_client.get('/api/v1/books/?search=second')

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # Verify data
    assert len(data['books']) == 1

    # Since I know this test should only return one value I can request
    #   the task from the list of tasks via its index
    book = data['books'][0]

    assert book['book_id'] == 2
    assert book['title'] == 'A Second Book'
    assert book['author_fname'] == 'King George'
    assert book['author_lname'] == 'II'
    assert book['publication_year'] == 1901
    assert book['checked_out_to'] == None


def test_update_book_by_id(flask_test_client):
    """Test updating a book record in the database via PUT request
    Args:
        flask_test_client: fixture function from conftest.py
    """
    
    # Add a new task to the list
    request = flask_test_client.post('/api/v1/books/', json={'title': 'A Book via Post', 
    'author_fname': 'Dr.', 'author_lname': 'Suess', 'publication_year': 2000,
    'checked_out_to': None})
    assert request.status_code == 200
    
    data = json.loads(request.data.decode())
    book_id = data['book_id']

    # Here is how to use the test client to simulate a PUT request
    request = flask_test_client.put(f'/api/v1/books/{book_id}/', json={'title': 'Updated Book', 
    'author_fname': 'Someone', 'author_lname': 'Awesome', 'publication_year': 2022,
    'checked_out_to': None})
    
    # Make sure we got a status code of 200
    assert request.status_code == 200

    data = json.loads(request.data.decode())
    assert book_id == data['book_id']

    request = flask_test_client.get(f'/api/v1/books/{book_id}/')
    data = json.loads(request.data.decode())

    book = data['books'][0]
    assert book['book_id'] == book_id
    assert book['title'] == 'Updated Book'
    assert book['author_fname'] == 'Someone'
    assert book['author_lname'] == 'Awesome'
    assert book['publication_year'] == 2022
    assert book['checked_out_to'] == None
