"""Database wrapper for the auth service.
"""

import sqlalchemy.exc as db_exc
from models import InvitationModel

from utils import SessionSingleton


class Wrapper:
    """Wrapper for the invitation service."""

    def __init__(self) -> None:
        self.session = SessionSingleton().get_session()

    def close(self) -> None:
        """Close session."""
        self.session.close()

    def get_invitations(self, user_id: int) -> list[dict]:
        """Get all invitations.

        Args:
            user_id (int): user id

        Returns:
            list[dict]: list of invitations
        """
        try:
            invitations = (
                self.session.query(InvitationModel)
                .filter(InvitationModel.user_id == user_id)
                .all()
            )
            return [invitation.__dict__ for invitation in invitations]
        except db_exc.NoResultFound as e:
            raise ValueError(f"Invitations not found: {e}") from e

    def create_invitation(self, user_id: int, event_id: int, invitee_id: int) -> None:
        """Create invitation.

        Args:
            user_id (int): user id
            event_id (int): event id
            invitee_id (int): invitee id
        """
        try:
            invitation = InvitationModel(user_id=user_id, event_id=event_id, invitee_id=invitee_id)
            self.session.add(invitation)
            self.session.commit()
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
