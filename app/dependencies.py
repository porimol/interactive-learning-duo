from fastapi import Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from jose import jwt
from passlib.context import CryptContext
from app.config import AUTH_SESSION_NAME, SECRET_KEY, ALGORITHM

templates = Jinja2Templates(directory="app/templates")
# Password hashing
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def check_authentication(request: Request):
    """
    Check if the request is authenticated.

    Args:
        request (Request): The incoming request.

    Raises:
        HTTPException: If the request is not authenticated.

    Returns:
        bool: True if the request is authenticated.
    """
    if not request.session.get(AUTH_SESSION_NAME):
        raise HTTPException(status_code=401, detail="Unauthorized url")
    return True


def is_authorized(auth_user: bool = Depends(check_authentication)):
    """
    Returns the authenticated user.

    Parameters:
    - auth_user (bool): A boolean value indicating whether the user is authenticated or not.

    Returns:
    - bool: The value of auth_user indicating the authentication status of the user.
    """
    return auth_user


def get_access_token(data: dict):
    """
    Generates an access token using the provided data.

    Args:
        data (dict): The data to be encoded in the access token.

    Returns:
        str: The encoded access token.
    """
    encoded_jwt = jwt.encode(data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_access_token(token: str) -> dict or Exception:
    """
    Decodes an access token to retrieve the original data.

    Args:
        token (str): The access token to be decoded.

    Returns:
        dict: The decoded data from the access token.
    """
    try:
        # token = request.session[AUTH_SESSION_NAME]
        decoded_data = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except Exception:
        # Handle token expiration error
        return Exception
 