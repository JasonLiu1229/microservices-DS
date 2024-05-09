"""Database wrapper for the auth service.
"""

import sqlalchemy.exc as db_exc
from models import UserModel

from utils import SessionSingleton


class Wrapper:
    """Wrapper for the auth service."""

    def __init__(self) -> None:
        self.session = SessionSingleton().get_session()

    def create_user(self, username: str, password: str) -> UserModel:
        """Create user.

        Args:
            username (str): username of user
            password (str): password of user

        Returns:
            UserModel: user model
        """
        try:
            user = UserModel(username=username, password=password)
            self.session.add(user)
            self.session.commit()
            return user
        except db_exc.OperationalError as e:
            self.session.rollback()
            raise ValueError(f"Failed to create user: {e}") from e

    def find_user(self, username: str) -> UserModel:
        """Find user.

        Args:
            username (str): username of user

        Returns:
            UserModel: user model
        """
        try:
            user = (
                self.session.query(UserModel)
                .filter(UserModel.username == username)
                .one()
            )
            return user
        except db_exc.NoResultFound as e:
            raise ValueError(f"User not found: {e}") from e

    def get_users(self) -> list[str]:
        """Get all users.

        Returns:
            list[str]: list of usernames
        """
        try:
            users = self.session.query(UserModel).all()
            return [user.username for user in users]
        except db_exc.NoResultFound as e:
            raise ValueError(f"Users not found: {e}") from e

    def get_password(self, username: str) -> str:
        """Get password.

        Args:
            username (str): username of user

        Returns:
            str: password
        """
        user = self.find_user(username)
        return user.password

    def check_user_exists(self, username: str) -> bool:
        """Check if user exists.

        Args:
            username (str): username of user

        Returns:
            bool: True if user exists, False otherwise
        """
        try:
            self.find_user(username)
            return True
        except ValueError:
            return False
        
    def get_user(self, user_id: int) -> dict:
        """Get user.

        Args:
            user_id (int): user id

        Returns:
            dict: user
        """
        try:
            user = (
                self.session.query(UserModel)
                .filter(UserModel.id == user_id)
                .one()
            )
            return user.__dict__
        except db_exc.NoResultFound as e:
            raise ValueError(f"User not found: {e}") from e

    def close(self) -> None:
        """Close session."""
        self.session.close()
