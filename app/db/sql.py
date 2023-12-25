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
    except sqlite3.Error as error:
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
    except sqlite3.Error as error:
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
    except sqlite3.Error as error:
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
    except sqlite3.Error as error:
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
    except sqlite3.Error as error:
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
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return error
    

def update_user_address(id, user_id, address):
    """
    Update a user's address in the database.

    Args:
        id (int): The ID of the user to update.
        user_id (int): The User ID of the user to update.
        address (str): The user's address.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO user_address(id, user_id, apartment, building, post_code, city, country) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       (id, user_id, address.get("apartment"), address.get("building"), address.get("post_code"), address.get("city"), address.get("country")))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return error


def count_user_address():
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
        cursor.execute("SELECT count(*) FROM user_address")
        address_count = cursor.fetchone()
        conn.close()
        if address_count:
            return address_count[0]
        return 0
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return error


def get_user_address_by_id(user_id):
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
        cursor.execute("SELECT * FROM user_address WHERE user_id=?", (user_id,))
        columns = [description[0] for description in cursor.description]
        user = cursor.fetchone()
        conn.close()
        if user:
            return dict(zip(columns, user))
        return {}
    except sqlite3.Error as error:
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
    except sqlite3.Error as error:
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
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return error
