"""Database wrapper for the events service.
"""

import sqlalchemy.exc as db_exc
from models import EventModel
from datetime import datetime

from utils import SessionSingleton


class Wrapper:
    """Wrapper for the events service."""

    def __init__(self) -> None:
        self.session = SessionSingleton().get_session()

    def close(self) -> None:
        """Close session."""
        self.session.close()

    def get_event(self, event_id: int) -> EventModel:
        """Get event.

        Args:
            event_id (int): event id

        Returns:
            dict: event
        """
        try:
            event = (
                self.session.query(EventModel).filter(EventModel.id == event_id).one()
            )
            return event
        except db_exc.NoResultFound as e:
            raise ValueError(f"Event not found: {e}") from e

    def get_events(self) -> list[EventModel]:
        """Get all events.

        Returns:
            dict: list of events
        """
        try:
            events = self.session.query(EventModel).all()
            return events
        except db_exc.NoResultFound as e:
            raise ValueError(f"Events not found: {e}") from e

    def create_event(
        self,
        organizer_id: int,
        title: str,
        description: str,
        date: datetime,
        is_public: bool,
    ) -> None:
        """Create event.

        Args:
            organizer_id (int): organizer id
            title (str): title of event
            description (str): description of event
            date (datetime): date of event
            is_public (bool): is event public
        """
        try:
            event = EventModel(
                organizer_id=organizer_id,
                title=title,
                description=description,
                date=date,
                is_public=is_public,
            )
            self.session.add(event)
            self.session.commit()
        except db_exc.OperationalError as e:
            self.session.rollback()
            raise ValueError(f"Failed to create event: {e}") from e
