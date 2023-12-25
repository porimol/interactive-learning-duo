from sqlite3 import Error
from app.db.sqlconn import connect_db


def get_question_stats(user_id):
    """
    Retrieves question statistics for a given user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of tuples containing the month name, question category, and question count.

    Raises:
        Error: If there is an error while connecting to the SQLite database.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        # cursor.execute("SELECT strftime('%m', created_at) AS month_name, question_category, COUNT(*) AS question_count FROM questions_answers WHERE user_id = ? GROUP BY strftime('%Y-%m', created_at), question_category;", (user_id,))
        cursor.execute("SELECT strftime('%m', created_at) AS month_name, question_category, COUNT(*) AS question_count FROM questions_answers WHERE user_id = ? GROUP BY strftime('%Y-%m', created_at);", (user_id,))
        user = cursor.fetchall()
        conn.close()
        return user
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error


def get_question_ratio(user_id):
    """
    Retrieves question statistics for a given user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of tuples containing the month name, question category, and question count.

    Raises:
        Error: If there is an error while connecting to the SQLite database.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT question_category, COUNT(*) AS question_count FROM questions_answers WHERE user_id = ? GROUP BY question_category;", (user_id,))
        user = cursor.fetchall()
        conn.close()
        return user
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error