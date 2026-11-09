
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

from app.config import get_settings

def get_database_path() -> Path:
    """Return the SQLite database path."""

    settings = get_settings()
    database_url = settings.DATABASE_URL

    if not database_url.startswith("sqlite:///"):
        raise ValueError("DATABASE_URL is not configured for SQLite.")

    database_path = Path(
        database_url.replace("sqlite:///", "", 1)
    )

    if not database_path.is_absolute():
        database_path = Path.cwd() / database_path

    database_path.parent.mkdir(parents=True, exist_ok=True)

    return database_path



def get_connection():
    """Create a database connection based on DATABASE_URL."""

    settings = get_settings()
    database_url = settings.DATABASE_URL

    if database_url.startswith("sqlite:///"):
        import sqlite3

        database_path = Path(
            database_url.replace("sqlite:///", "", 1)
        )

        if not database_path.is_absolute():
            database_path = Path.cwd() / database_path

        database_path.parent.mkdir(parents=True, exist_ok=True)

        connection = sqlite3.connect(database_path, timeout=30)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        return connection

    if database_url.startswith(("postgresql://", "postgres://")):
        return psycopg.connect(
            database_url,
            row_factory=dict_row,
            connect_timeout=15,
        )

    raise ValueError(
        "Unsupported DATABASE_URL. Use SQLite or PostgreSQL."
    )
