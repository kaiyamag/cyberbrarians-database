import json


# By using the parameter flask_test_client, we automatically get access to a "fake" version
#   of our webservice application to test our api. This is provided by the pytest fixture in conftest.py
#   (note the parameter name matches the name of the fixture function).
def test_posting_a_patron(flask_test_client):

    # Simulate a post request that sends json data
    request = flask_test_client.post('api/v1/patrons/', json={'first_name': 'Kaiya', 
    'last_name': 'Magnuson', 'account_type': 'STUDENT'})

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # The body of the response is JSON, so we turn it from a string into a JSON
    #   object. The json object can be treated similarly to a dictionary or list
    #   based on the format of the JSON content.
    data = json.loads(request.data.decode())

    assert data['status'] == "success"
    assert data['account_id'] == 1

    request = flask_test_client.post('api/v1/patrons/', json={'first_name': 'Tobin', 
    'last_name': 'Chin', 'account_type': 'AWESOME DEVELOPER'})

    # Make sure we got a status code of 412: precondition failed on account_type
    assert request.status_code == 412

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    assert data['account_type'] == 'AWESOME DEVELOPER'

    request = flask_test_client.post('api/v1/patrons/', json={'first_name': 'Imaginary', 
    'last_name': 'Friend', 'account_type': 'STUDENT'})

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    assert data['account_id'] == 2


def test_get_all_patrons(flask_test_client):
    
    # Here is how to use the test client to simulate a GET request
    request = flask_test_client.get('/api/v1/patrons/')

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # Verify data
    assert len(data['patrons']) == 2

    # When getting all the tasks, we cannot rely on the ordering because I did
    #   not enforce an ordering on the SQL query. Always be careful with
    #   assumptions about order unless you have explicity
    #   ensured that the content will be ordered
    for patrons in data['patrons']:
        if patrons['account_id'] == 1:
            assert patrons['first_name'] == 'Kaiya'
            assert patrons['last_name'] == 'Magnuson'
            assert patrons['account_type'] == 'STUDENT'
        elif patrons['account_id'] == 2:
            assert patrons['first_name'] == 'Imaginary'
            assert patrons['last_name'] == 'Friend'
            assert patrons['account_type'] == 'STUDENT'
        else:
            # We should not get here as there are only two items inserted
            raise Exception("Unknown patron found in database!")


def test_get_patron_by_id(flask_test_client):
    
    # Here is how to use the test client to simulate a GET request
    request = flask_test_client.get('/api/v1/patrons/1/')

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    # Make sure we got a status code of 200
    assert request.status_code == 200

    assert len(data['patrons']) == 1

    # Get the first item from the list of tasks (which should only be task id 1)
    patron = data['patrons'][0]

    # Check the id and description
    assert patron['first_name'] == 'Kaiya'
    assert patron['last_name'] == 'Magnuson'
    assert patron['account_type'] == 'STUDENT'


def test_get_patron_by_last_name_search(flask_test_client):

    # Here is how to use the test client to simulate a GET request with a query string
    request = flask_test_client.get('/api/v1/patrons/?search=magnus')

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # Verify data
    assert len(data['patrons']) == 1

    # Since I know this test should only return one value I can request
    #   the task from the list of tasks via its index
    patron = data['patrons'][0]

    assert patron['first_name'] == 'Kaiya'
    assert patron['last_name'] == 'Magnuson'
    assert patron['account_type'] == 'STUDENT'


# NOTE: This test is causing the test of test_bookdb to not finish?

# def test_update_patron_by_id(flask_test_client):
    
#     # Add a new patron to the list
#     request = flask_test_client.post('/api/v1/patrons/', json={'first_name': 'Nikola', 
#     'last_name': 'Tesla', 'account_type': 'STAFF'})
#     assert request.status_code == 200
    
#     data = json.loads(request.data.decode())
#     account_id = data['account_id']

#     # Here is how to use the test client to simulate a PUT request
#     request = flask_test_client.put(f'/api/v1/patrons/{account_id}/', json={'first_name': 'Thomas', 
#     'last_name': 'Edison', 'account_type': 'PROFESSOR'})
    
#     # Make sure we got a status code of 200
#     assert request.status_code == 200

#     data = json.loads(request.data.decode())
#     assert account_id == data['account_id']

#     request = flask_test_client.get(f'/api/v1/patrons/{account_id}/')
#     data = json.loads(request.data.decode())

#     patron = data['patrons'][0]
#     assert patron['account_id'] == account_id
#     assert patron['first_name'] == 'Thomas'
#     assert patron['last_name'] == 'Edison'
#     assert patron['account_type'] == 'PROFESSOR'
