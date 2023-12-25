import sqlite3


def connect_db():
    """
    Connects to the SQLite database and returns a cursor object.

    Returns:
        cursor: A cursor object for executing SQL queries on the database.
    """
    try:
        conn = sqlite3.connect('pythonqa.db')
        return conn
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return error
