from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
from api.course_api import Course, CourseDB
from api.book_api import BookDB
from models.library import Library

course_list_blueprint = Blueprint('course_list_blueprint', __name__)


@course_list_blueprint.route('/course-entry')
def course_entry():
   database = BookDB(g.mysql_db, g.mysql_cursor)
   return render_template("course-entry.html", books=database.select_all_books())


@course_list_blueprint.route('/course-entry', methods=["POST"])
def add_course():
    course_title = request.form.get("course_title")
    course_reference_book = request.form.get("course_reference_book")
    
    new_course = Course(course_title, course_reference_book)
    database = CourseDB(g.mysql_db, g.mysql_cursor)

    database.insert_course(new_course)

    return redirect('/')


@course_list_blueprint.route('/course-list', methods=["GET"])
def list_courses():
    database = CourseDB(g.mysql_db, g.mysql_cursor)

    return render_template('course-list.html', course_table=database.select_all_courses())


@course_list_blueprint.route('/course-update', methods=["GET", "POST"])
def select_courses_to_edit():
    course_database = CourseDB(g.mysql_db, g.mysql_cursor)

    if request.method == "POST":
        course_id = request.form.get("course_id")
        new_course_title = request.form.get("course_title")
        new_reference_book = request.form.get("course_reference_book")
        course_database.update_course(course_id, Course(new_course_title, new_reference_book))
        return redirect('/')

    book_database = BookDB(g.mysql_db, g.mysql_cursor)
    return render_template(
        '/course-update.html',
        books=book_database.select_all_books(),
        courses=course_database.select_all_courses()
    )


@course_list_blueprint.route('/course-remove', methods=['GET', 'POST'])
def course_delete():
    database = CourseDB(g.mysql_db, g.mysql_cursor)

    if request.method == 'POST':
        course_id_to_delete = request.form.get("course_id_to_delete")
        database.delete_course_by_id(course_id_to_delete)
        return redirect('/')

    return render_template(
        '/course-remove.html',
        courses=database.select_all_courses()
    )