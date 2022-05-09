"""
book_view.py

Collection of functions performing CRUD operations on book records for a
given route
"""

from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
from api.book_api import Book, BookDB
from models.library import Library

book_list_blueprint = Blueprint('book_list_blueprint', __name__)

@book_list_blueprint.route('/', methods=["GET", "POST"])
def index():
    """No GET or POST requests are made from the index route, so this function
    simply renders index.html 
    """
    # database = BookDB(g.mysql_db, g.mysql_cursor)

    # # We know that if a POST is made from index (/), then that was the user
    # # selecting the 'Checkout Books' button
    # if request.method == "POST":
    #     book_ids = request.form.getlist("book_item")

    #     for book_id in book_ids:
    #         database.delete_book_by_id(book_id) 

    # return render_template('index.html', book_list=database.select_all_books())
    return render_template('index.html')


@book_list_blueprint.route('/book-entry')
def book_entry():
   """Renders the book-entry.html page
   """

   return render_template('book-entry.html')


@book_list_blueprint.route('/add-book', methods=["POST"])
def add_book():
    """Add a new book to the databse

    Returns:
        render_template: redirects user to the index route
    """

    book_title = request.form.get("book_title")
    book_author_fname = request.form.get("book_author_fname")
    book_author_lname = request.form.get("book_author_lname")
    book_publication_year = request.form.get("book_publication_year")
    
    new_book = Book(book_title, book_author_fname, book_author_lname, book_publication_year, None)
    database = BookDB(g.mysql_db, g.mysql_cursor)

    database.insert_book(new_book)

    return redirect('/')


@book_list_blueprint.route('/book-checkout-selection')
def book_checkout_selection():
    """Renders checkout-book.html page with a list of all books available for
    checkout
    """

    database = BookDB(g.mysql_db, g.mysql_cursor)

    return render_template('checkout-book.html', book_list=database.select_available_books())


@book_list_blueprint.route('/checkout-book', methods=["POST"])
def checkout_book():
    """Updates a book record to be checked-out to a patron.

    Returns:
        render_template: If successful, renders a checkout-success.html page,
        if failed, renders a checkout-failure.html page
    """

    database = BookDB(g.mysql_db, g.mysql_cursor)
    my_library = Library(g.mysql_db, g.mysql_cursor)

    # We know that if a POST is made from this route, then that was the user
    # selecting the 'Checkout Books' button
    if request.method == "POST":
        book_ids = request.form.getlist("book_item")
        patron_id = request.form.get("id")
        book_list = []
    
        for book_id in book_ids:
            new_book = my_library.checkout_book(patron_id, book_id)

            if new_book[0] == False:
                return render_template('checkout-failure.html', book_list=book_list, 
                error_message=new_book[1])

            book_list.append(new_book[1])
        
        return render_template('checkout-success.html', book_list=book_list)


@book_list_blueprint.route('/book-list', methods=["GET", "POST"])
def patron_list():
    database = BookDB(g.mysql_db, g.mysql_cursor)

    return render_template('book-list.html', book_table=database.select_all_books())   

 
  