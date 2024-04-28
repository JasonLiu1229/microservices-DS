from sqlalchemy import Column, SmallInteger, String
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class"""



class UserModel(Base):
    """
    Model representing a user.
    """

    __tablename__ = "users"

    id = Column(SmallInteger, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
