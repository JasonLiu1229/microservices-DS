"""Database wrapper for the participation service.
"""

from enum import Enum

import sqlalchemy.exc as db_exc
from models import ParticipationModel

from utils import SessionSingleton


class ParticipationStatus(Enum):
    """Participation status."""

    ACCEPTED = "accepted"
    DECLINED = "declined"
    MAYBE = "maybe"


class Wrapper:
    """Wrapper for the participation service."""

    def __init__(self) -> None:
        self.session = SessionSingleton().get_session()

    def close(self) -> None:
        """Close session."""
        self.session.close()
    
    def get_participation(self, participation_id: int) -> ParticipationModel:
        """Get participation.

        Args:
            participation_id (int): participation id

        Returns:
            ParticipationModel: participation
        """
        try:
            participation = (
                self.session.query(ParticipationModel)
                .filter(ParticipationModel.id == participation_id)
                .one()
            )
            return participation
        except db_exc.NoResultFound as e:
            raise ValueError(f"Participation not found: {e}") from e
        
    def get_all_participations(self) -> list[ParticipationModel]:
        """Get all participations.
        
        Returns:
            list[ParticipationModel]: list of participations
        """
        try:
            participations = self.session.query(ParticipationModel).all()
            return participations
        except db_exc.NoResultFound as e:
            raise ValueError(f"Participations not found: {e}") from e

    def get_participations(self, user_id: int) -> list[ParticipationModel]:
        """Get all participations.

        Args:
            user_id (int): user id

        Returns:
            list[dict]: list of participations
        """
        try:
            participations = (
                self.session.query(ParticipationModel)
                .filter(ParticipationModel.user_id == user_id)
                .all()
            )
            return participations
        except db_exc.NoResultFound as e:
            raise ValueError(f"Participations not found: {e}") from e
    
    def get_participations_by_event(self, event_id: int) -> list[ParticipationModel]:
        """Get all participations.

        Args:
            event_id (int): event id

        Returns:
            list[ParticipationModel]: list of participations based on event id
        """
        try:
            participations = (
                self.session.query(ParticipationModel)
                .filter(ParticipationModel.event_id == event_id)
                .all()
            )
            return participations
        except db_exc.NoResultFound as e:
            raise ValueError(f"Participations not found: {e}") from e
        
    def get_participations_by_user_event(
        self, user_id: int, event_id: int
    ) -> ParticipationModel:
        """Get all participations.

        Args:
            user_id (int): user id
            event_id (int): event id

        Returns:
            ParticipationModel: participation
        """
        try:
            participation = (
                self.session.query(ParticipationModel)
                .filter(ParticipationModel.user_id == user_id)
                .filter(ParticipationModel.event_id == event_id)
                .one()
            )
            return participation
        except db_exc.NoResultFound as e:
            raise ValueError(f"Participation not found: {e}") from e

    def create_participation(
        self, user_id: int, event_id: int, status: str
    ) -> ParticipationModel:
        """Create participation.

        Args:
            user_id (int): user id
            event_id (int): event id
            status (str): participation status

        Returns:
            ParticipationModel: participation model
        """
        try:
            participation = ParticipationModel(
                user_id=user_id, event_id=event_id, status=status
            )
            self.session.add(participation)
            self.session.commit()
            return participation
        except db_exc.SQLAlchemyError as e:
            raise ValueError(f"Failed to create participation: {e}") from e

    def update_participation(self, participation_id: int, status: str) -> None:
        """Update participation status.

        Args:
            participation_id (int): participation id
            status (str): participation status
        """
        try:
            participation = (
                self.session.query(ParticipationModel)
                .filter(ParticipationModel.id == participation_id)
                .one()
            )
            participation.status = status
            self.session.commit()
        except db_exc.NoResultFound as e:
            raise ValueError(f"Participation not found: {e}") from e
        except db_exc.SQLAlchemyError as e:
            raise ValueError(f"Failed to update participation: {e}") from e
