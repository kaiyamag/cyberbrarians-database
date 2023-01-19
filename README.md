# The Cyberbrary

## Description
This application is a simple library management application for a school like the College of Wooster. Our library management application tracks  books in the library, library patrons, and textbooks required by courses at the school. A user can add books and patrons to the library, check out books, return books and create courses with assigned textbooks. In addition, the application supports creating, reading, updating, and deleting books, patrons, and courses via the HTML interface and the API routes described below.

## Launching The Project in a Virtual Environment
	1. Create virtual environment in the project directory: $python -m venv env   
	2. Activate virtual environment: $env\scripts\activate    
	3. Install required libraries: $pip install -r requirements.txt
	4. Initialize database: $flask initdb
	5. Run webpage: $flask run
	
Please see IMPORTANT.md for more detailed instructions
 
## API Documentation
The following API routes are available to interact with the application:

**BOOKS:**


GET from `/api/v1/books/`
* /books/ returns a list of all books as dictionaries 
* /books/{book_id} returns the book with the corresponding book_id
* /books/?search="search term" returns a list of books with a title matching the search term

POST from `/api/v1/books/`
* Adds a book record to the database. Must post an entire book as a dictionary, including all fields:
	+ Title
	+ Author_fname
	+ Author_lname
	+ Publication_year
	+ Checked_out_to (which should be null for newly created books)
For example: 
    ``{'title': 'My Favorite Book', 'author_fname': 'Nobody', 'author_lname': 'In particular', 'publication_year': 1999, 'checked_out_to': None}``
	
POST from `/api/v1/books/<int:patron_id>/<int:book_id>`
* Assigns the book selected by book_id to the patron selected by patron_id to be checked out.

PUT from `/api/v1/books/<int:book_id>`
* Updates the book with the corresponding book_id. Must put an entire book (as explained above) which will replace the attributes of the book with the given book_id

DELETE from `/api/v1/books/<int:book_id>`
* Deletes the book with the corresponding book_id.

POST from ``/api/v1/books/<int:patron_id>/<int:book_id>/``
* Checks out the book with the given book_id to the patron indicated by the patron_id

POST from ``/api/v1/books/return-book/<int:book_id>/``
* Returns the book indicated by the given book_id if that book was checked out. **This function is currently deactivated.**

**PATRONS:**


GET from `/api/v1/patrons/`
* /patrons/ returns a list of all patrons as dictionaries 
* /patrons/{account_id} returns the patron with the corresponding patron_id
* /patrons/?search="search term" returns a list of patrons with a last name matching the search term. **This function is currently deactivated.**

POST from `/api/v1/patrons/`
* Adds a patron record to the database. Must post a patron as a dictionary, including all fields:
	+ First_name
	+ Last_name
	+ Account_type (can only be 'STUDENT', 'PROFESSOR', or 'STAFF')
For example: 
    ``{'first_name': 'Kaiya', 'last_name': 'Magnuson', 'account_type': 'STUDENT'}``

PUT from `/api/v1/patrons/<int:account_id>`
* Updates the patron with the corresponding account_id. Must put an entire patron (as explained above) which will replace the attributes of the patron with the given patron_id

DELETE from `/api/v1/patrons/<int:account_id>`
* Deletes the patron with the corresponding account_id.


**Courses:**


GET from `/api/v1/coursess/`
* /courses/ returns a list of all courses as dictionaries 
* /courses/{account_id} returns the course with the corresponding course_id
* /courses/?search="search term" returns a list of courses with a course title matching the search term

POST from `/api/v1/courses/`
* Adds a course record to the database. Must post a patron as a dictionary, including all fields:
	+ course_title
	+ reference_book (must be a book_id of a book currently in the books table)
For example: 
    ``{'course_title': 'Intro to Ceramics', 'reference_book': 1}``

PUT from `/api/v1/courses/<int:course_id>`
* Updates the course with the corresponding course_id. Must put an entire course (as explained above) which will replace the attributes of the course with the given course_id

DELETE from `/api/v1/courses/<int:course_id>`
* Deletes the course with the corresponding course_id.