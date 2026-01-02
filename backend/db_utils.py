import os
from urllib.parse import urlparse, urlunparse

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError

load_dotenv()

def create_database_if_not_exists():
    """
    Check if the database exists, and create it if it doesn't.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    parsed_url = urlparse(database_url)
    database_name = parsed_url.path.lstrip('/')

    if not database_name:
        raise ValueError("Database name not found in DATABASE_URL")

    server_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        '/postgres',
        parsed_url.params,
        parsed_url.query,
        parsed_url.fragment
    ))

    try:
        server_engine = create_engine(server_url, isolation_level="AUTOCOMMIT")

        with server_engine.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                {"dbname": database_name}
            )
            exists = result.scalar() is not None

            if not exists:
                print(f"Database '{database_name}' does not exist. Creating...")
                conn.execute(text(f'CREATE DATABASE "{database_name}"'))
                print(f"Database '{database_name}' created successfully.")
            else:
                print(f"Database '{database_name}' already exists.")

        server_engine.dispose()

    except (OperationalError, ProgrammingError) as e:
        print(f"Error checking/creating database: {e}")
        raise
