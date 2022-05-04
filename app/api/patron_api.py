"""
patron_api.py

Routes for the API and logic for managing patrons.
"""

from flask import g, request, jsonify, Blueprint

from models.patron import Patron, PatronDB

# Establish the blueprint to link it to the flask app file (main_app.py)
#   Need to do this before you create your routes
patron_api_blueprint = Blueprint("patron_api_blueprint", __name__)


# Define routes for the API
#   Note that we can stack the decorators to associate similar routes to the same function.
#   In the case below we can optionally add the id number for a patron to the end of the url
#   so we can retrieve a specific patron or the entire list of patrons as a JSON object
@patron_api_blueprint.route('/api/v1/patrons/', defaults={'account_id':None}, methods=["GET"])
@patron_api_blueprint.route('/api/v1/patrons/<int:account_id>/', methods=["GET"])
def get_patrons(account_id):
    """
    get_patrons can take urls in a variety of forms:
        * /api/v1/patron/ - get all patrons
        * /api/v1/patron/1 - get the patron with id 1 (or any other valid id)
        * /api/v1/patron/?search="eggs" - find all patrons with the string "eggs" anywhere in the description
            * The ? means we have a query string which is essentially a list of key, value pairs
                where the ? indicates the start of the query string parameters and the pairs are separated
                by ampersands like so:
                ?id=10&name=Sarah&job=developer
            * The query string is optional 
    """

    # To access a query string, we need to get the arguments from our web request object
    args = request.args
    
    # setup the patronDB object with the mysql connection and cursor objects
    patrondb = PatronDB(g.mysql_db, g.mysql_cursor)

    result = None
    
    # If an ID for the patron is not supplied then we are either returning all
    #   patrons or any patrons that match the search query string.
    if account_id is None:
        # Logic to find all or multiple patrons

        # Since the args for the query string are in the form of a dictionary, we can
        #   simply check if the key is in the dictionary. If not, the web request simply
        #   did not supply this information.
        if not 'search' in args:
            result = patrondb.select_all_patrons()
        # All patrons matching the query string "search"
        else:
            result = patrondb.select_all_patrons_by_last_name(args['search'])
    
    else:
        # Logic to request a specific patron
        # We get a specific patrons based on the provided patron ID
        result = patrondb.select_patron_by_id(account_id)

    # Sending a response of JSON including a human readable status message,
    #   list of the patrons found, and a HTTP status code (200 OK).
    return jsonify({"status": "success", "patrons": result}), 200


"""
@patron_api_blueprint.route('/api/v1/patrons/', methods=["POST"])
def add_patron():
    patrondb = patronDB(g.mysql_db, g.mysql_cursor)
        
    patron = patron(request.json['description'])
    result = patrondb.insert_patron(patron)
    
    return jsonify({"status": "success", "id": result['n']}), 200


@patron_api_blueprint.route('/api/v1/patrons/<int:n>/', methods=["PUT"])
def update_patron(n):
    patrondb = patronDB(g.mysql_db, g.mysql_cursor)

    patron = patron(request.json['description'])
    patrondb.update_patron(n, patron)
    
    return jsonify({"status": "success", "id": n}), 200


@patron_api_blueprint.route('/api/v1/patrons/<int:n>/', methods=["DELETE"])
def delete_patron(n):
    patrondb = patronDB(g.mysql_db, g.mysql_cursor)

    patrondb.delete_patron_by_id(n)
        
    return jsonify({"status": "success", "id": n}), 200
"""