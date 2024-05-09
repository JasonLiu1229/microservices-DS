from sqlalchemy import Column, SmallInteger, String, Boolean

# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class"""


class EventModel(Base):
    """
    Model representing an event.
    """

    __tablename__ = "events"

    id = Column(SmallInteger, primary_key=True, autoincrement=True, nullable=False)
    organizer_id = Column(SmallInteger, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date = Column(String, nullable=False)
    is_public = Column(Boolean, nullable=False, default=False)
