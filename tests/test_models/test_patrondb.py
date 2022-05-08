from app.models.patron import Patron, PatronDB

# By using the parameter db_test_client, we automatically get access to our test
#   database provided by the pytest fixture in conftest.py
#   (note the parameter name matches the name of the fixture function).
def test_patron_insert(db_test_client):
    conn, cursor = db_test_client
    patrondb = PatronDB(conn, cursor)

    patrondb.insert_patron(Patron("Agatha", "Christie", "PROFESSOR"))
    
    result = patrondb.select_patron_by_id(1)[0]
    assert result['first_name'] == "Agatha"
    assert result['last_name'] == "Christie"
    assert result['account_type'] == "PROFESSOR"
    conn.commit()


def test_patron_delete(db_test_client):
    conn, cursor = db_test_client
    patrondb = PatronDB(conn, cursor)
    
    patrondb.insert_patron(Patron("Delete", "Me", "STAFF"))

    result = patrondb.select_patron_by_id(2)[0]
    assert result['first_name'] == "Delete"

    patrondb.delete_patron_by_id(2)
    result = patrondb.select_patron_by_id(2)
    assert len(result) == 0
    conn.commit()
