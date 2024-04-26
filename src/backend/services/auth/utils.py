"""Utils for the auth service.
"""

import os

from sqlalchemy import URL


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
    user = get_env_variable("APP_DB_USER")
    password = get_env_variable("APP_DB_PASSWORD")
    host = get_env_variable("APP_DB_HOST")
    port = get_env_variable("APP_DB_PORT_USERS")
    database_name = get_env_variable("APP_DB_NAME_USERS")

    return URL.create(
        drivername="postgresql+psycopg2",
        username=user,
        password=password,
        host=host,
        port=port,
        database=database_name,
    )
