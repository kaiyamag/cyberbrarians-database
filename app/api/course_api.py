"""
course_api.py

Routes for the API and logic for managing Courses.
"""

from flask import g, request, jsonify, Blueprint

from models.course import Course, CourseDB

# Establish the blueprint to link it to the flask app file (main_app.py)
#   Need to do this before you create your routes
course_api_blueprint = Blueprint("course_api_blueprint", __name__)


# Define routes for the API
#   Note that we can stack the decorators to associate similar routes to the same function.
#   In the case below we can optionally add the id number for a task to the end of the url
#   so we can retrieve a specific task or the entire list of tasks as a JSON object
@course_api_blueprint.route('/api/v1/courses/', defaults={'course_id':None}, methods=["GET"])
@course_api_blueprint.route('/api/v1/course/<int:course_id>/', methods=["GET"])
def get_courses(course_id):
    """
    get_courses can take urls in a variety of forms:
        * /api/v1/courses/ - get all tasks
        * /api/v1/courses/1 - get the task with id 1 (or any other valid id)
        * /api/v1/courses/?search="eggs" - find all tasks with the string "eggs" anywhere in the description
            * The ? means we have a query string which is essentially a list of key, value pairs
                where the ? indicates the start of the query string parameters and the pairs are separated
                by ampersands like so:
                ?id=10&name=Sarah&job=developer
            * The query string is optional 
    """

    # To access a query string, we need to get the arguments from our web request object
    args = request.args
    
    # setup the TaskDB object with the mysql connection and cursor objects
    coursedb = CourseDB(g.mysql_db, g.mysql_cursor)

    result = None
    
    # If an ID for the task is not supplied then we are either returning all
    #   tasks or any tasks that match the search query string.
    if course_id is None:
        # Logic to find all or multiple tasks

        # Since the args for the query string are in the form of a dictionary, we can
        #   simply check if the key is in the dictionary. If not, the web request simply
        #   did not supply this information.
        if not 'search' in args:
            result = coursedb.select_all_courses()
        # All tasks matching the query string "search"
        else:
            result = coursedb.select_all_courses_by_title(args['search'])
    
    else:
        # Logic to request a specific task
        # We get a specific tasks based on the provided task ID
        result = coursedb.select_course_by_id(course_id)

    # Sending a response of JSON including a human readable status message,
    #   list of the tasks found, and a HTTP status code (200 OK).
    return jsonify({"status": "success", "courses": result}), 200


@course_api_blueprint.route('/api/v1/courses/', methods=["POST"])
def add_course():
    coursedb = CourseDB(g.mysql_db, g.mysql_cursor)
        
    course = Course(request.json['course_title'], request.json['reference_book'])      # NOTE: Do we need to add all fields?
    course_id = coursedb.insert_course(course)['course_id']
    
    return jsonify({"status": "success", "course_id": course_id}), 200


# @task_api_blueprint.route('/api/v1/tasks/<int:task_id>/', methods=["PUT"])
# def update_task(task_id):
#     taskdb = TaskDB(g.mysql_db, g.mysql_cursor)

#     task = Task(request.json['description'])
#     taskdb.update_task(task_id, task)
    
#     return jsonify({"status": "success", "id": task_id}), 200


@course_api_blueprint.route('/api/v1/courses/<int:course_id>/', methods=["DELETE"])
def delete_course(course_id):
    coursedb = CourseDB(g.mysql_db, g.mysql_cursor)

    coursedb.delete_course_by_id(course_id)
        
    return jsonify({"status": "success", "course_id": course_id}), 200
