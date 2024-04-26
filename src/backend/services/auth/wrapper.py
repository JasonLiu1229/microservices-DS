"""Database wrapper for the auth service.
"""

from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import get_database_url


session_maker = sessionmaker(bind=create_engine(get_database_url()))
session = session_maker()


class UserModel(BaseModel):
    """
    Class for user model.
    """

    username: str
    email: str
    full_name: str
    disabled: bool = None
    role: str = None
    password: str
