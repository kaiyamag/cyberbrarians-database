from app.models.book import Book, BookDB

# By using the parameter db_test_client, we automatically get access to our test
#   database provided by the pytest fixture in conftest.py
#   (note the parameter name matches the name of the fixture function).
def test_book_insert(db_test_client):
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


# def test_task_delete(db_test_client):
#     conn, cursor = db_test_client
#     taskdb = TaskDB(conn, cursor)
    
#     taskdb.insert_task(Task("Delete Me!"))

#     result = taskdb.select_task_by_id(2)[0]
#     assert result['description'] == "Delete Me!"

#     taskdb.delete_task_by_id(2)
#     result = taskdb.select_task_by_id(2)
#     assert len(result) == 0
#     conn.commit()
