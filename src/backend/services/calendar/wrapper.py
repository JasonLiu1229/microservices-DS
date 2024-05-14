"""Database wrapper for the calendar service.
"""

import sqlalchemy.exc as db_exc

from models import CalendarModel

from utils import SessionSingleton


class Wrapper:
    """Wrapper for the calendar service."""

    def __init__(self) -> None:
        self.session = SessionSingleton().get_session()

    def close(self) -> None:
        """Close session."""
        self.session.close()

    def get_all_calendar_shared(self) -> list[CalendarModel]:
        """Get all shared calendars.

        Returns:
            list[CalendarModel]: list of shared calendars
        """
        try:
            calendars = self.session.query(CalendarModel).all()
            return calendars
        except db_exc.NoResultFound as e:
            raise ValueError(f"Calendars not found: {e}") from e

    def get_calendar(self, calendar_id: int) -> CalendarModel:
        """Get calendar shared based on calendar id.

        Args:
            calendar_id (int): calendare share id

        Returns:
            CalendarModel: calendar model which is shared
        """
        try:
            calendar = (
                self.session.query(CalendarModel)
                .filter(CalendarModel.id == calendar_id)
                .one()
            )
            return calendar
        except db_exc.NoResultFound as e:
            raise ValueError(f"Calendar not found: {e}") from e

    def get_shared_calendars(self, user_id: int) -> list[CalendarModel]:
        """Get all shared calendars.

        Args:
            user_id (int): user id

        Returns:
            list[CalendarModel]: list of shared calendars
        """
        try:
            calendars = (
                self.session.query(CalendarModel)
                .filter(CalendarModel.user_id == user_id)
                .all()
            )
            return calendars
        except db_exc.NoResultFound as e:
            raise ValueError(f"Calendars not found: {e}") from e

    def create_share(self, user_id: int, share_id: int) -> CalendarModel:
        """Share calendar.

        Args:
            user_id (int): user id
            share_id (int): user id of whom you sharing the calendar with
        """
        try:
            calendar = CalendarModel(user_id=user_id, share_id=share_id)
            self.session.add(calendar)
            self.session.commit()
            return calendar
        except db_exc.OperationalError as e:
            self.session.rollback()
            raise ValueError(f"Failed to share calendar: {e}") from e
