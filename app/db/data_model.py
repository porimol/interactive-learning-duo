from pydantic import BaseModel
from pydantic import EmailStr


class Token(BaseModel):
    """
    Represents a token object.

    Attributes:
        access_token (str): The access token.
        token_type (str): The type of the token.
    """
    
    access_token: str
    token_type: str


class UserAuth(BaseModel):
    """
    Represents user authentication information.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    email: EmailStr
    password: str


class UserData(BaseModel):
    """
    Represents user authentication information.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    password: str
