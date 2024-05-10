"""Models for the participation service."""

from sqlalchemy import Column, Enum, SmallInteger

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class"""


class ParticipationModel(Base):
    """
    Model representing a participation.
    """

    __tablename__ = "participations"

    id = Column(SmallInteger, primary_key=True, autoincrement=True, nullable=False)
    event_id = Column(SmallInteger, nullable=False)
    user_id = Column(SmallInteger, nullable=False)
    status = Column(Enum("accepted", "declined", "maybe"), nullable=False)
