from sqlite3 import Error
from app.db.sqlconn import connect_db


def create_user(first_name, last_name, email, password):
    """
    Registers a user in the database.

    Args:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address.
        password (str): The user's password.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(first_name, last_name, email, password) VALUES (?, ?, ?, ?)",
                    (first_name, last_name, email, password))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error


def get_all_users():
    """
    Retrieve all users from the database.

    Returns:
        list: A list of tuples representing the users.
              Each tuple contains the user's information.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        return users
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error


def get_user_by_email(email):
    """
    Retrieve a user from the database by their email.

    Args:
        id (int): The email of the user to retrieve.

    Returns:
        dict: A dictionary containing the user's information, with column names as keys.

    Raises:
        sqlite3.Error: If there is an error while connecting to the SQLite database.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        columns = [description[0] for description in cursor.description]
        user = cursor.fetchone()
        conn.close()
        if user:
            return dict(zip(columns, user))
        return {}
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error


def get_user_by_id(user_id):
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
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        columns = [description[0] for description in cursor.description]
        user = cursor.fetchone()
        conn.close()
        user = dict(zip(columns, user))
        return user
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error


def update_user(user_id, first_name, last_name, email):
    """
    Update a user in the database.

    Args:
        id (int): The ID of the user to update.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address.
        password (str): The user's password.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET first_name=?, last_name=?, email=? WHERE id=?",
                    (first_name, last_name, email, user_id))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error


def get_photo_by_user_id(user_id):
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
        cursor.execute("SELECT photo FROM users WHERE id=?", (user_id,))
        columns = [description[0] for description in cursor.description]
        user = cursor.fetchone()
        conn.close()
        user = dict(zip(columns, user))
        return user
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error


def update_photo(user_id, photo):
    """
    Update a user's photo in the database.

    Args:
        id (int): The ID of the user to update.
        photo (str): The user's photo.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET photo=? WHERE id=?", (photo, user_id))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error


def update_password(user_id, new_password):
    """
    Update a user in the database.

    Args:
        id (int): The ID of the user to update.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address.
        password (str): The user's password.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error
