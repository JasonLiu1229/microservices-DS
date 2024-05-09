from sqlalchemy import Column, SmallInteger, Enum
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

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
    status = Column(Enum("pending", "accepted", "declined", "maybe"), nullable=False, default="pending")
