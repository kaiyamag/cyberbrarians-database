from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
from api.patron_api import Patron, PatronDB

patron_table_blueprint = Blueprint('patron_table_blueprint', __name__)

# REMOVED PATRON INDEX ROUTE

# @patron_table_blueprint.route('/', methods=["GET", "POST"])
# def index():
#     database = PatronDB(g.mysql_db, g.mysql_cursor)

#     if request.method == "POST":
#         # DEBUG
#         print("Got a POST request")

#         patron_ids = request.form.getlist("account_id")
#         for patron_id in patron_ids:
#             database.delete_patron_by_id(patron_id)

#     # DEBUG
#     print(database.select_all_patrons())

#     return render_template('index.html', patron_table=database.select_all_patrons())    


@patron_table_blueprint.route('/patron-entry')
def patron_entry():

   return render_template("patron-entry.html")


@patron_table_blueprint.route('/add-patron', methods=["POST"])
def add_patron():
    patron_first_name = request.form.get("patron_first_name")
    patron_last_name = request.form.get("patron_last_name")
    patron_account_type = request.form.get("patron_account_type")
    
    new_patron = Patron(patron_first_name, patron_last_name, patron_account_type)
    database = PatronDB(g.mysql_db, g.mysql_cursor)

    # Check that patron account type is valid.
    # NOTE: The client is not informed of an error if they input the wrong type
    if new_patron._account_type in ['STUDENT', 'PROFESSOR', 'STAFF']:
        database.insert_patron(new_patron)

    return redirect('/')
'''
@patron_table_blueprint.route('/update-patron', method=["PUT"])
def update_patron():
    patron_first_name = request.form.get("patron_first_name")
    patron_last_name = request.form.get("patron_last_name")
    patron_account_type = request.form.get("patron_account_type")

    updated_patron = Patron(patron_first_name, patron_last_name, patron_account_type)
    database = PatronDB(g.mysql_db, g.mysql_cursor)

    database.update_patron_by_id()

    return redirect('/')
    '''

@patron_table_blueprint.route('/patron-list', methods=["GET", "POST"])
def patron_list():
    database = PatronDB(g.mysql_db, g.mysql_cursor)

    if request.method == "POST":
        # DEBUG
        print("Got a POST request")

        patron_ids = request.form.getlist("account_id")
        for patron_id in patron_ids:
            database.delete_patron_by_id(patron_id)


    return render_template('patron-list.html', patron_table=database.select_all_patrons())   
