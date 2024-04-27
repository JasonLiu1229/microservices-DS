"""Database wrapper for the auth service.
"""

import sqlalchemy.exc as db_exc
from models import TokenModel, UserModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import get_database_url


session_maker = sessionmaker(bind=create_engine(get_database_url()))
session = session_maker()


def create_user(username: str, password: str) -> UserModel:
    """Create user.

    Args:
        username (str): username of user
        password (str): password of user

    Returns:
        UserModel: user model
    """
    try:
        user = UserModel(username=username, password=password)
        session.add(user)
        session.commit()
        return user
    except db_exc.OperationalError as e:
        session.rollback()
        raise ValueError(f"Failed to create user: {e}") from e


def find_user(username: str) -> UserModel:
    """Find user.

    Args:
        username (str): username of user

    Returns:
        UserModel: user model
    """
    try:
        user = session.query(UserModel).filter(UserModel.username == username).one()
        return user
    except db_exc.NoResultFound as e:
        raise ValueError(f"User not found: {e}") from e


def get_users() -> list[str]:
    """Get all users.

    Returns:
        list[str]: list of usernames
    """
    try:
        users = session.query(UserModel).all()
        return [user.username for user in users]
    except db_exc.NoResultFound as e:
        raise ValueError(f"Users not found: {e}") from e


def add_token(token: str, user_id: int) -> TokenModel:
    """Add token to user.

    Args:
        token (str): token to add
        user_id (int): user id to add token to

    Returns:
        TokenModel: token model
    """
    try:
        token_instance = TokenModel(token=token, user_id=user_id)
        session.add(token_instance)
        session.commit()
        return token_instance
    except db_exc.OperationalError as e:
        session.rollback()
        raise ValueError(f"Failed to add token: {e}") from e


def del_token(token: str) -> None:
    """Delete token, is not a real delete, it just makes the token invalid for the user.

    Args:
        token (str): token to delete
    """
    try:
        token_instance = (
            session.query(TokenModel).filter(TokenModel.token == token).one()
        )
        token_instance.valid = False
        session.commit()
    except db_exc.NoResultFound as e:
        raise ValueError(f"Token not found: {e}") from e

def get_token(token: str) -> TokenModel:
    """Get token.

    Args:
        token (str): token to get

    Returns:
        TokenModel: token model
    """
    try:
        token_instance = (
            session.query(TokenModel).filter(TokenModel.token == token).one()
        )
        return token_instance
    except db_exc.NoResultFound as e:
        raise ValueError(f"Token not found: {e}") from e
