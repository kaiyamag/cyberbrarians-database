from asyncio.windows_events import NULL
from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
from api.course_api import Course, CourseDB
from models.library import Library

course_list_blueprint = Blueprint('course_list_blueprint', __name__)


@course_list_blueprint.route('/course-entry')
def course_entry():
   return render_template("course-entry.html")


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

"""
@course_list_blueprint.route('/course-update-select', methods=["GET", "POST"])
def select_courses_to_edit():
    course_id = request.form.get("course_id")
    database = CourseDB(g.mysql_db, g.mysql_cursor)
    return render_template('/course-update-modify-form')


@course_list_blueprint.route('/course-update-modify-form', methods=["GET", "POST"])
def update_courses():
    
    database = CourseDB(g.mysql_db, g.mysql_cursor)

    return redirect()
    """