from sqlalchemy import Column, SmallInteger, String
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class"""
