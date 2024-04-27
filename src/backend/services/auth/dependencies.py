"""
Dependencies for the API.

This module contains all the dependencies for the API, such as the security and roles.
"""

# Imports
import datetime

from exceptions import (
    CREDENTIALS_EXECPTION,
    EXPIRED_EXCEPTION,
    INVALID_EXCEPTION_TOKEN,
    NOT_FOUND_EXCEPTION_TOKEN,
)

from typing import Annotated, Any

import bcrypt
import jwt
from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from wrapper import find_user, get_token, get_users, UserModel


# Constants
# openssl rand -hex 32
SECRET_KEY = "de64ecaae7dce6487be8fba54b71749449dd76638e2784b49e7bf31757307052"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
LOWEST_ROLE = "default"


class Token(BaseModel):
    """
    Class for token.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Class for token data.
    """

    username: str


# oauth2_scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# sync Functions
def verify_password(plain_password: str, crypt_password: str) -> bool:
    """Verify input password with hashed password.

    Args:
        plain_password (str): input password
        crypt_password (str): hashed password

    Returns:
        bool: True if password is correct, False otherwise
    """
    return bcrypt.checkpw(plain_password.encode(), crypt_password.encode())


def get_password_hash(password: str) -> str:
    """Get password hash.

    Args:
        password (str): password

    Returns:
        str: hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def authenticate_user(username: str, password: str) -> UserModel | None:
    """Authenticate user.

    Args:
        username (str): username of the user
        password (str): password of the user

    Returns:
        UserModel | None: User model if user is authenticated, None otherwise
    """
    for user in get_users():
        if user.username == username and verify_password(password, str(user.password)):
            return user
    return None


def create_access_token(data: dict[str, Any], expires_delta: datetime.timedelta) -> Any:
    """Create access token.

    Args:
        data (dict[str, Any]): data to encode
        expires_delta (datetime.timedelta): expiration time

    Returns:
        Any: encoded token
    """
    to_encode = data.copy()
    expire = datetime.datetime.now() + (
        expires_delta if expires_delta else datetime.timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# async Functions
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> Any:
    """Get current user.

    Args:
        token (Annotated[str, Depends): token for user that depends on oauth2_scheme

    Raises:
        credentials_exception: If the credentials are invalid or the user is not found
        expired_exception: If the token has expired

    Returns:
        Any: _description_
    """

    # decode token and get username and role
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if (username := payload.get("username")) is None:
            raise CREDENTIALS_EXECPTION
    except jwt.ExpiredSignatureError as exc:
        raise EXPIRED_EXCEPTION from exc
    except jwt.PyJWTError as exc:
        raise CREDENTIALS_EXECPTION from exc

    # get user from token_data
    if (user := find_user(username=username)) is None:
        raise CREDENTIALS_EXECPTION

    return user


async def check_token_validity(token: str) -> None:
    """Check token validity.

    Args:
        token (str): token to check

    Raises:
        HTTPException: If token is invalid
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        password: str = payload.get("password")

        # check if username is found
        if username is None or find_user(username=username) is None:
            raise CREDENTIALS_EXECPTION
        if password is None:
            raise CREDENTIALS_EXECPTION

        # check if token does not exist
        if not (token_instance := get_token(token)):
            raise NOT_FOUND_EXCEPTION_TOKEN
        # check if token is invalid
        if not token_instance.valid:
            raise INVALID_EXCEPTION_TOKEN
    except jwt.ExpiredSignatureError as exc:
        raise EXPIRED_EXCEPTION from exc
    except jwt.PyJWTError as exc:
        raise CREDENTIALS_EXECPTION from exc


async def get_current_active_user(
    current_user: Annotated[UserModel, Security(get_current_user)]
) -> Any:
    """Get current active user.

    Args:
        current_user (Annotated[UserModel, Security]): current user

    Returns:
        Any: User model
    """
    return current_user
