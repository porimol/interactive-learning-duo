import qdrant_client


def qvectordb(host: str, port: int, username: str, password: str) -> None:
    """
    Connects to a Qdrant vector database.

    Args:
        host (str): The hostname or IP address of the Qdrant vector database.
        port (int): The port number of the Qdrant vector database.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        None
    """
    # Connect to the Qdrant vector database using the provided credentials
    client = qdrant_client.Client(
        host=host,
        port=port,
        username=username,
        password=password
    )
    client.connect()
    
