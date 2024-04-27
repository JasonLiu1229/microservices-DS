"""Utils for the auth service.
"""

import os

from sqlalchemy import create_engine, Engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


def get_env_variable(name: str) -> str:
    """
    Get environment variable.

    :param name: Name of the environment variable
    :return: Value of the environment variable
    """
    return os.getenv(name, "")


def get_database_url() -> URL:
    """
    Get database URL.

    :return: Database URL
    """
    user = get_env_variable("POSTGRES_DB_USER")
    password = get_env_variable("POSTGRES_DB_PASSWORD")
    host = get_env_variable("POSTGRES_DB_HOST")
    port = get_env_variable("POSTGRES_DB_PORT")
    database_name = get_env_variable("POSTGRES_DB")

    return URL.create(
        drivername="postgresql+psycopg2",
        username=user,
        password=password,
        host=host,
        port=port,
        database=database_name,
    )


def get_engine() -> Engine:
    """
    Get database engine.

    :return: Database engine
    """
    return create_engine(get_database_url())


def get_session() -> Session:
    """
    Get database session.

    :return: Database session
    """
    return sessionmaker(bind=get_engine())()


class SessionSingleton:
    """
    Singleton for the database session.
    """

    _session = None

    @classmethod
    def get_session(cls) -> Session:
        """
        Get the database session.

        :return: Database session
        """
        if cls._session is None:
            cls._session = get_session()
        return cls._session
