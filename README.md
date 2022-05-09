# Final Project Name

## Description

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
    {'title': 'My Favorite Book', 'author_fname': 'Nobody', 'author_lname': 'In particular', 'publication_year': 1999, 'checked_out_to': None}
	
POST from `/api/v1/books/<int:patron_id>/<int:book_id>`
	* Assigns the book selected by book_id to the patron selected by patron_id to be checked out.

PUT from `/api/v1/books/<int:book_id>`
	* Updates the book with the corresponding book_id. Must put an entire book (as explained above) which will replace the attributes of the book with the given book_id

DELETE from `/api/v1/books/<int:book_id>`
	* Deletes the book with the corresponding book_id.

**PATRONS:**
GET from `/api/v1/patrons/`
	* /patrons/ returns a list of all patrons as dictionaries 
	* /patrons/{account_id} returns the patron with the corresponding patron_id
	* /patrons/?search="search term" returns a list of patrons with a last name matching the search term

POST from `/api/v1/patrons/`
	* Adds a patron record to the database. Must post an patron book as a dictionary, including all fields:
		+ First_name
		+ Last_name
		+ Account_type (can only be 'STUDENT', 'PROFESSOR', or 'STAFF')
For example: 
    {'first_name': 'Kaiya', 'last_name': 'Magnuson', 'account_type': 'STUDENT'}

PUT from `/api/v1/patrons/<int:account_id>`
	* Updates the patron with the corresponding account_id. Must put an entire patron (as explained above) which will replace the attributes of the patron with the given patron_id

DELETE from `/api/v1/patrons/<int:account_id>`
	* Deletes the patron with the corresponding account_id.

