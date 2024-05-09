"""Database wrapper for the auth service.
"""

import sqlalchemy.exc as db_exc

from utils import SessionSingleton


class Wrapper:
    """Wrapper for the participation service."""

    def __init__(self) -> None:
        self.session = SessionSingleton().get_session()

    def close(self) -> None:
        """Close session."""
        self.session.close()
