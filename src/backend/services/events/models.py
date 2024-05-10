"""Models for the event service."""

from sqlalchemy import Boolean, Column, SmallInteger, String, Date

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
    is_public = Column(Boolean, nullable=False, default=False)
    date = Column(Date, nullable=False)
