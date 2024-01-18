from sqlite3 import Error
from app.db.sqlconn import connect_db


def get_qa_categories():
    """
    Retrieve all question categories from the database.

    Returns:
        list: A list of tuples representing the question categories.
              Each tuple contains the category ID and category name.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM question_category")
        categories = cursor.fetchall()
        conn.close()
        return categories
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error


def get_qa_category_byid(category_id):
    """
    Retrieve a question category by its ID from the database.

    Args:
        category_id (int): The ID of the category to retrieve.

    Returns:
        dict: A dictionary representing the retrieved category, with column names as keys.

    Raises:
        Error: If there is an error while connecting to the SQLite database.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM question_category WHERE id=?", (category_id,))
        columns = [description[0] for description in cursor.description]
        category = cursor.fetchone()
        conn.close()
        category = dict(zip(columns, category))
        return category
    except Error as error:
        print("Error while connecting to SQLite", error)
        return error
