from sqlite3 import Error
from app.db.sqlconn import connect_db


def insert_question(user_id, question, answer, question_category, created_at):
    """
    Insert a new question into the database.

    Args:
        user_id (int): The ID of the user who asked the question.
        question (str): The question text.
        answer (str): The answer to the question.
        question_category (str): The category of the question.
        created_at (str): The timestamp when the question was created.

    Returns:
        bool: True if the question was successfully inserted, False otherwise.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO questions_answers(user_id, question, answer, question_category, created_at) VALUES (?, ?, ?, ?, ?)",
                    (user_id, question, answer, question_category, created_at))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error


def get_todays_qa_by_userid(user_id, created_at):
    """
    Retrieve a user from the database by their ID.

    Args:
        id (int): The ID of the user to retrieve.

    Returns:
        dict: A dictionary containing the user's information, with column names as keys.

    Raises:
        sqlite3.Error: If there is an error while connecting to the SQLite database.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions_answers WHERE user_id=? AND DATE(created_at)=? ORDER BY id DESC", (user_id, created_at,))
        # columns = [description[0] for description in cursor.description]
        user = cursor.fetchall()
        conn.close()
        # user = dict(zip(columns, user))
        return user
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error
