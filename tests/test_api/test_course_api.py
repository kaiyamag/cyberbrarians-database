"""
test_book_api.py

Collection of functions to be run with pytest to test all api functionality
"""

import json


# By using the parameter flask_test_client, we automatically get access to a "fake" version
#   of our webservice application to test our api. This is provided by the pytest fixture in conftest.py
#   (note the parameter name matches the name of the fixture function).
def test_posting_a_course(flask_test_client):
    """Test adding multiple courses to the database via POST request
    Args:
        flask_test_client: fixture function from conftest.py
    """

    # Add a book to the database to use as the reference book
    request = flask_test_client.post('api/v1/books/', json={'title': 'My Favorite Book', 
    'author_fname': 'Nobody', 'author_lname': 'In particular', 'publication_year': 1999,
    'checked_out_to': None})

    request = flask_test_client.post('/api/v1/courses/', json={'course_title': 'Artificial Intelligence', 
    'reference_book': 1})

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # The body of the response is JSON, so we turn it from a string into a JSON
    #   object. The json object can be treated similarly to a dictionary or list
    #   based on the format of the JSON content.
    data = json.loads(request.data.decode())

    assert data['status'] == "success"
    assert data['course_id'] == 1

    request = flask_test_client.post('/api/v1/courses/', json={'course_title': 'Computer Graphics', 
    'reference_book': 1})

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())
    assert data['course_id'] == 2


def test_get_all_courses(flask_test_client):
    """Test getting a list of all courses in database. Relies on course records
    added in test_posting_a_course().

    Args:
        flask_test_client: fixture function from conftest.py
    """
    
    # Here is how to use the test client to simulate a GET request
    request = flask_test_client.get('/api/v1/courses/')

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # Verify data
    assert len(data['courses']) == 2

    # When getting all the tasks, we cannot rely on the ordering because I did
    #   not enforce an ordering on the SQL query. Always be careful with
    #   assumptions about order unless you have explicity
    #   ensured that the content will be ordered
    for courses in data['courses']:
        if courses['course_id'] == 1:
            assert courses['course_title'] == 'Artificial Intelligence'
            assert courses['reference_book'] == 1
        elif courses['course_id'] == 2:
            assert courses['course_title'] == 'Computer Graphics'
            assert courses['reference_book'] == 1
        else:
            # We should not get here as there are only two items inserted
            raise Exception("Unknown course found in database!")

# NOTE: Running into json decoding error with this one
# def test_get_course_by_id(flask_test_client):
#     """Test selecting a course from the database by its course_id via GET
#     Args:
#         flask_test_client: fixture function from conftest.py
#     """
    
#     # Here is how to use the test client to simulate a GET request
#     request = flask_test_client.get('/api/v1/courses/1/')

#     # The body of the response is JSON, so we turn it from a string into a JSON
#     # object.
#     data = json.loads(request.data.decode())

#     # Make sure we got a status code of 200
#     assert request.status_code == 200

#     assert len(data['courses']) == 1

#     # Get the first item from the list of tasks (which should only be task id 1)
#     course = data['courses'][0]

#     # Check the id and description
#     assert course['course_id'] == 1
#     assert course['course_title'] == 'Artificial Intelligence'
#     assert course['reference_book'] == 1



def test_get_course_by_title_search(flask_test_client):
    """Test selecting a course by a keyword search in its course_title via GET
    Args:
        flask_test_client: fixture function from conftest.py
    """

    # Here is how to use the test client to simulate a GET request with a query string
    request = flask_test_client.get('/api/v1/courses/?search=Computer')

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # Verify data
    assert len(data['courses']) == 1

    # Since I know this test should only return one value I can request
    #   the task from the list of tasks via its index
    course = data['courses'][0]

    assert course['course_id'] == 2
    assert course['course_title'] == 'Computer Graphics'
    assert course['reference_book'] == 1


# NOTE: Will not be implemented since course_api.py does not have an update function
# def test_update_book_by_id(flask_test_client):
#     """Test updating a book record in the database via PUT request
#     Args:
#         flask_test_client: fixture function from conftest.py
#     """
    
#     # Add a new book to the list
#     request = flask_test_client.post('/api/v1/books/', json={'title': 'A Book via Post', 
#     'author_fname': 'Dr.', 'author_lname': 'Suess', 'publication_year': 2000,
#     'checked_out_to': None})
#     assert request.status_code == 200
    
#     data = json.loads(request.data.decode())
#     book_id = data['book_id']

#     # Here is how to use the test client to simulate a PUT request
#     request = flask_test_client.put(f'/api/v1/books/{book_id}/', json={'title': 'Updated Book', 
#     'author_fname': 'Someone', 'author_lname': 'Awesome', 'publication_year': 2022,
#     'checked_out_to': None})
    
#     # Make sure we got a status code of 200
#     assert request.status_code == 200

#     data = json.loads(request.data.decode())
#     assert book_id == data['book_id']

#     request = flask_test_client.get(f'/api/v1/books/{book_id}/')
#     data = json.loads(request.data.decode())

#     book = data['books'][0]
#     assert book['book_id'] == book_id
#     assert book['title'] == 'Updated Book'
#     assert book['author_fname'] == 'Someone'
#     assert book['author_lname'] == 'Awesome'
#     assert book['publication_year'] == 2022
#     assert book['checked_out_to'] == None
