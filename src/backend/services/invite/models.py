"""
Models for the invitation service.
"""

from sqlalchemy import Column, Enum, SmallInteger

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class"""


class InvitationModel(Base):
    """
    Model representing an invitation.
    """

    __tablename__ = "invitations"

    id = Column(SmallInteger, primary_key=True, autoincrement=True, nullable=False)
    event_id = Column(SmallInteger, nullable=False)
    user_id = Column(SmallInteger, nullable=False)
    invitee_id = Column(SmallInteger, nullable=False)
    status = Column(
        Enum("pending", "accepted", "declined", "maybe"),
        nullable=False,
        default="pending",
    )
