from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
from api.course_api import Course, CourseDB
from models.library import Library

course_list_blueprint = Blueprint('course_list_blueprint', __name__)


@course_list_blueprint.route('/course-entry')
def course_entry():
   return render_template('course-entry.html')


@course_list_blueprint.route('/add-course', methods=["POST"])
def add_course():
    course_title = request.form.get("course_title")
    course_reference_book = request.form.get("course_reference_book")
    
    new_course = Course(course_title, course_reference_book)
    database = CourseDB(g.mysql_db, g.mysql_cursor)

    database.insert_course(new_course)

    return redirect('/')

  