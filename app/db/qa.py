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
        cursor.execute("INSERT INTO questions_answers(user_id, question, answer, question_category_id, created_at) VALUES (?, ?, ?, ?, ?)",
                    (user_id, question, answer, question_category, created_at))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error


def get_qa_histories(user_id):
    """
    Retrieve the question and answer histories for a given user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of tuples representing the question and answer histories.
              Each tuple contains the following elements:
              - id (int): The ID of the question/answer.
              - user_id (int): The ID of the user.
              - question (str): The question.
              - answer (str): The answer.
              - category_name (str): The name of the question category.
              - created_at (str): The timestamp when the question/answer was created.

    Raises:
        Error: If there is an error while connecting to the database.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT qa.id, u.first_name, u.last_name, qa.question, qa.answer, qc.category_name, qa.created_at 
                       FROM questions_answers qa INNER JOIN question_category qc on qa.question_category_id=qc.id 
                       INNER JOIN users u on qa.user_id=u.id
                       WHERE user_id=? ORDER BY qa.id DESC""", (user_id,))
        qa_histories = cursor.fetchall()
        conn.close()
        return qa_histories
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
        cursor.execute("""SELECT qa.id, qa.user_id, qa.question, qa.answer, qc.category_name, qa.created_at 
                       FROM questions_answers qa INNER JOIN question_category qc on qa.question_category_id=qc.id 
                       WHERE user_id=? AND DATE(qa.created_at)=? ORDER BY qa.id DESC""", (user_id, created_at,))
        user = cursor.fetchall()
        conn.close()
        return user
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error


def delete_qa_by_id(qa_id: int, user_id: int):
    """
    Delete a question and its corresponding answer from the database based on the question ID and user ID.

    Args:
        qa_id (int): The ID of the question to be deleted.
        user_id (int): The ID of the user who posted the question.

    Returns:
        list: A list containing the details of the deleted question and answer, including the question ID, user ID,
              question text, answer text, category name, and creation date. If an error occurs, the error message is returned.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        response = cursor.execute("DELETE FROM questions_answers WHERE id=? AND user_id=?", (qa_id, user_id,))
        conn.commit()
        conn.close()
        return response
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error
