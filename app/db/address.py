from sqlite3 import Error
from app.db.sqlconn import connect_db
    

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
    except Error as error:
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
    except Error as error:
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
    except Error as error:
        print("Error while connecting to sqlite", error)
        return error