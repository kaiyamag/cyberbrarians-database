from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
from api.book_api import Book, BookDB

book_list_blueprint = Blueprint('book_list_blueprint', __name__)

@book_list_blueprint.route('/', methods=["GET", "POST"])
def index():
    database = BookDB(g.mysql_db, g.mysql_cursor)

    if request.method == "POST":
        book_ids = request.form.getlist("book_item")
        for book_id in book_ids:
            database.delete_book_by_id(book_id)

    return render_template('index.html', book_list=database.select_all_books())    


@book_list_blueprint.route('/book-entry')
def book_entry():
   return render_template("book-entry.html")


@book_list_blueprint.route('/add-book', methods=["POST"])
def add_book():
    book_title = request.form.get("book_title")
    book_author_fname = request.form.get("book_author_fname")
    book_author_lname = request.form.get("book_author_lname")
    book_publication_year = request.form.get("book_publication_year")
    
    new_book = Book(book_title, book_author_fname, book_author_lname, book_publication_year)
    database = BookDB(g.mysql_db, g.mysql_cursor)

    database.insert_book(new_book)

    return redirect('/')