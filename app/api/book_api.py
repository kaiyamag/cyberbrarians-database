"""
book_api.py

Routes for the API and logic for managing Books.
"""

from flask import g, request, jsonify, Blueprint

from models.book import Book, BookDB

# Establish the blueprint to link it to the flask app file (main_app.py)
#   Need to do this before you create your routes
book_api_blueprint = Blueprint("book_api_blueprint", __name__)


# Define routes for the API
#   Note that we can stack the decorators to associate similar routes to the same function.
#   In the case below we can optionally add the id number for a task to the end of the url
#   so we can retrieve a specific task or the entire list of tasks as a JSON object
@book_api_blueprint.route('/api/v1/books/', defaults={'book_id':None}, methods=["GET"])
@book_api_blueprint.route('/api/v1/book/<int:book_id>/', methods=["GET"])
def get_books(book_id):
    """
    get_books can take urls in a variety of forms:
        * /api/v1/book/ - get all tasks
        * /api/v1/book/1 - get the task with id 1 (or any other valid id)
        * /api/v1/book/?search="eggs" - find all tasks with the string "eggs" anywhere in the description
            * The ? means we have a query string which is essentially a list of key, value pairs
                where the ? indicates the start of the query string parameters and the pairs are separated
                by ampersands like so:
                ?id=10&name=Sarah&job=developer
            * The query string is optional 
    """

    # To access a query string, we need to get the arguments from our web request object
    args = request.args
    
    # setup the TaskDB object with the mysql connection and cursor objects
    bookdb = BookDB(g.mysql_db, g.mysql_cursor)

    result = None
    
    # If an ID for the task is not supplied then we are either returning all
    #   tasks or any tasks that match the search query string.
    if book_id is None:
        # Logic to find all or multiple tasks

        # Since the args for the query string are in the form of a dictionary, we can
        #   simply check if the key is in the dictionary. If not, the web request simply
        #   did not supply this information.
        if not 'search' in args:
            result = bookdb.select_all_books()
        # All tasks matching the query string "search"
        else:
            result = bookdb.select_all_books_by_title(args['search'])
    
    else:
        # Logic to request a specific task
        # We get a specific tasks based on the provided task ID
        result = bookdb.select_book_by_id(book_id)

    # Sending a response of JSON including a human readable status message,
    #   list of the tasks found, and a HTTP status code (200 OK).
    return jsonify({"status": "success", "books": result}), 200


@book_api_blueprint.route('/api/v1/books/', methods=["POST"])
def add_book():
    bookdb = BookDB(g.mysql_db, g.mysql_cursor)
        
    book = Book(request.json['title'], request.json['author_fname'], 
    request.json['author_lname'], request.json['publication_year'],
    request.json['checked_out_to'])      

    new_book_id = bookdb.insert_book(book)['book_id']
    
    return jsonify({"status": "success", "id": new_book_id}), 200


@book_api_blueprint.route('/api/v1/book/<int:book_id>/', methods=["PUT"])
def update_book(book_id):
    bookdb = BookDB(g.mysql_db, g.mysql_cursor)

    book = Book(request.json['title'], request.json['author_fname'], 
    request.json['author_lname'], request.json['publication_year'], 
    request.json['checked_out_to'])

    bookdb.update_book(book_id, book)
    
    return jsonify({"status": "success", "id": book_id}), 200


@book_api_blueprint.route('/api/v1/books/<int:book_id>/', methods=["DELETE"])
def delete_book(book_id):
    bookdb = BookDB(g.mysql_db, g.mysql_cursor)

    bookdb.delete_book_by_id(book_id)
        
    return jsonify({"status": "success", "id": book_id}), 200


@book_api_blueprint.route('/api/v1/books/<int:library_member_id>/<int:book_id>/', methods=["POST"])
def checkout_book():
    bookdb = BookDB(g.mysql_db, g.mysql_cursor)
    my_library = Library(g.mysql_db, g.mysql_cursor)
        
    book = my_library.checkout_book(library_member_id, book_id) 
    if new_book[0] == False:
        # Conflict: the book could not be checked out
        return jsonify({"status": "failure", "library_member_id": result['libray_member_id'], 
        "book_id": result['book_id']}), 409 
    else:
        return jsonify({"status": "success", "library_member_id": result['libray_member_id'], 
        "book_id": result['book_id']}), 200
