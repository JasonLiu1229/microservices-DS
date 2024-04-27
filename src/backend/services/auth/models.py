from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
)

Base = declarative_base()

class UserModel(Base):
    """
    Model representing a user.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    
    token_ids = relationship("TokenModel", back_populates="user", cascade="all, delete")

class TokenModel(Base):
    """
    Class for token model for database.
    """
    
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    token = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    valid = Column(Boolean, nullable=False, default=True)

    user = relationship("UserModel", back_populates="token_ids")
