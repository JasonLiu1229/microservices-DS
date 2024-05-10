"""Models for the calendar service."""

from sqlalchemy import Column, SmallInteger

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class"""


class CalendarModel(Base):
    """
    Model representing a calendar.
    """

    __tablename__ = "calendar_shares"

    id = Column(SmallInteger, primary_key=True, autoincrement=True, nullable=False)
    owner_id = Column(SmallInteger, nullable=False)
    shared_with_id = Column(SmallInteger, nullable=False)
