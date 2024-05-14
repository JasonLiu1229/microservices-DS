"""Database wrapper for the invite service.
"""

from enum import Enum

import sqlalchemy.exc as db_exc
from models import InvitationModel

from utils import SessionSingleton


class InvitationStatus(Enum):
    """Invitation status."""

    PENDING = ("pending",)
    ACCEPTED = "accepted"
    DECLINED = "declined"
    MAYBE = "maybe"


class Wrapper:
    """Wrapper for the invitation service."""

    def __init__(self) -> None:
        self.session = SessionSingleton().get_session()

    def close(self) -> None:
        """Close session."""
        self.session.close()
        
    def get_all_invitations(self) -> list[InvitationModel]:
        """Get all invitations.

        Returns:
            list[InvitationModel]: list of invitations
        """
        try:
            invitations = self.session.query(InvitationModel).all()
            return invitations
        except db_exc.NoResultFound as e:
            raise ValueError(f"Invitations not found: {e}") from e

    def get_invitations(self, user_id: int) -> list[InvitationModel]:
        """Get all invitations.

        Args:
            user_id (int): user id

        Returns:
            list[InvitationModel]: list of invitations
        """
        try:
            invitations = (
                self.session.query(InvitationModel)
                .filter(InvitationModel.invitee_id == user_id)
                .all()
            )
            return invitations
        except db_exc.NoResultFound as e:
            raise ValueError(f"Invitations not found: {e}") from e

    def create_invitation(
        self, user_id: int, event_id: int, invitee_id: int
    ) -> InvitationModel:
        """Create invitation.

        Args:
            user_id (int): user id
            event_id (int): event id
            invitee_id (int): invitee id

        Returns:
            InvitationModel: invitation model
        """
        try:
            invitation = InvitationModel(
                user_id=user_id, event_id=event_id, invitee_id=invitee_id
            )
            self.session.add(invitation)
            self.session.commit()
            return invitation
        except db_exc.OperationalError as e:
            self.session.rollback()
            raise ValueError(f"Failed to create invitation: {e}") from e

    def delete_invitation(self, invitation_id: int) -> None:
        """Delete invitation.

        Args:
            invitation_id (int): invitation id
        """
        try:
            invitation = (
                self.session.query(InvitationModel)
                .filter(InvitationModel.id == invitation_id)
                .one()
            )
            self.session.delete(invitation)
            self.session.commit()
        except db_exc.NoResultFound as e:
            raise ValueError(f"Invitation not found: {e}") from e
        except db_exc.OperationalError as e:
            self.session.rollback()
            raise ValueError(f"Failed to delete invitation: {e}") from e

    def update_invitation(self, invitation_id: int, status: InvitationStatus) -> None:
        """Update invitation.

        Args:
            invitation_id (int): invitation id
            status (str): invitation status
        """
        try:
            invitation = (
                self.session.query(InvitationModel)
                .filter(InvitationModel.id == invitation_id)
                .one()
            )
            invitation.status = status
            self.session.commit()
        except db_exc.NoResultFound as e:
            raise ValueError(f"Invitation not found: {e}") from e
        except db_exc.OperationalError as e:
            self.session.rollback()
            raise ValueError(f"Failed to update invitation: {e}") from e

    def get_invite(self, invite_id: int) -> InvitationModel:
        """Get invite.

        Args:
            invite_id (int): invite id

        Returns:
            dict: invite
        """
        try:
            invite = (
                self.session.query(InvitationModel)
                .filter(InvitationModel.id == invite_id)
                .one()
            )
            return invite
        except db_exc.NoResultFound as e:
            raise ValueError(f"Invite not found: {e}") from e
