
import sqlite3
from pathlib import Path

from app.config import get_settings


def get_database_path() -> Path:
    """Get the SQLite database file path."""
    settings = get_settings()

    if not settings.DATABASE_URL.startswith("sqlite:///"):
        raise ValueError("Only SQLite database URLs are supported.")

    database_path = Path(
        settings.DATABASE_URL.replace("sqlite:///", "", 1)
    )

    if not database_path.is_absolute():
        database_path = Path.cwd() / database_path

    database_path.parent.mkdir(parents=True, exist_ok=True)

    return database_path


def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite database connection."""
    connection = sqlite3.connect(
        get_database_path(),
        timeout=30,
    )

    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection
