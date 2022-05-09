"""
test_bookdb.py

Collection of functions to test the interface with the book database in book.py
"""

from app.models.book import Book, BookDB

# By using the parameter db_test_client, we automatically get access to our test
#   database provided by the pytest fixture in conftest.py
#   (note the parameter name matches the name of the fixture function).
def test_book_insert(db_test_client):
    """Test that a book record is correctly added to the database

    Args:
        db_test_client: fixture function from conftest.py
    """

    # The test fixture only setups the 
    conn, cursor = db_test_client
    bookdb = BookDB(conn, cursor)

    bookdb.insert_book(Book("A Famous Book", "George", "Washington", 1980, None))
    
    result = bookdb.select_book_by_id(1)[0]
    assert result['title'] == "A Famous Book"
    assert result['author_fname'] == "George"
    assert result['author_lname'] == "Washington"
    assert result['publication_year'] == 1980
    assert result['checked_out_to'] == None
    conn.commit()


def test_book_delete(db_test_client):
    """Test that a book record is correctly deleted from the database

    Args:
        db_test_client: fixture function from conftest.py
    """
    
    conn, cursor = db_test_client
    bookdb = BookDB(conn, cursor)
    
    bookdb.insert_book(Book("Delete Me!", "William", "Shakespeare", 2013, None))

    result = bookdb.select_book_by_id(2)[0]
    assert result['title'] == "Delete Me!"

    bookdb.delete_book_by_id(2)
    result = bookdb.select_book_by_id(2)
    assert len(result) == 0
    conn.commit()
