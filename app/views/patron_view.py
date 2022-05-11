from cgitb import html
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


@patron_table_blueprint.route('/patron-entry', methods=["POST"])
def add_patron():
    patron_first_name = request.form.get("patron_first_name")
    patron_last_name = request.form.get("patron_last_name")
    patron_account_type = request.form.get("account_type")
    
    new_patron = Patron(patron_first_name, patron_last_name, patron_account_type)
    database = PatronDB(g.mysql_db, g.mysql_cursor)

    # Check that patron account type is valid.
    # NOTE: The client is not informed of an error if they input the wrong type
    if new_patron._account_type in ['STUDENT', 'PROFESSOR', 'STAFF']:
        database.insert_patron(new_patron)

    return redirect('/')


@patron_table_blueprint.route('/patron-update', methods=["GET", "POST"])
def edit_patrons():
    patron_database = PatronDB(g.mysql_db, g.mysql_cursor)

    if request.method == "POST":
        account_id = request.form.get("account_id")
        new_patron_first_name = request.form.get("patron_first_name")
        new_patron_last_name = request.form.get("patron_last_name")
        new_account_type = request.form.get("account_type")
        patron_database.update_patron_by_id(account_id, Patron(new_patron_first_name, new_patron_last_name, new_account_type))
        return redirect('/')

    return render_template(
        '/patron-update.html',
        patrons=patron_database.select_all_patrons()
    )


@patron_table_blueprint.route('/patron-list', methods=["GET", "POST"])
def patron_list():
    database = PatronDB(g.mysql_db, g.mysql_cursor)

    return render_template('patron-list.html', patron_table=database.select_all_patrons())   


@patron_table_blueprint.route('/patron-remove', methods=['GET', 'POST'])
def patron_delete():
    database = PatronDB(g.mysql_db, g.mysql_cursor)

    if request.method == 'POST':
        account_id_to_delete = request.form.get("account_id_to_delete")
        database.delete_patron_by_id(account_id_to_delete)
        return redirect('/')

    return render_template(
        '/patron-remove.html',
        patrons=database.select_all_patrons()
    )