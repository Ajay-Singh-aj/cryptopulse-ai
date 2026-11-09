
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from app.config import get_settings


def get_timezone() -> ZoneInfo:
    """Return the configured application timezone."""
    settings = get_settings()
    return ZoneInfo(settings.TIMEZONE)


def get_current_datetime() -> datetime:
    """Get the current date and time in the configured timezone."""
    return datetime.now(get_timezone())


def get_current_date():
    """Get today's date in the configured timezone."""
    return get_current_datetime().date()


def get_utc_datetime() -> datetime:
    """Get the current UTC datetime."""
    return datetime.now(timezone.utc)


def format_datetime(value: datetime) -> str:
    """Format a datetime in the configured timezone."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)

    return value.astimezone(get_timezone()).strftime(
        "%d %b %Y, %I:%M %p %Z"
    )
