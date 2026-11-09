
import re
from urllib.parse import urlparse, urlunparse


def clean_text(value: str | None) -> str:
    """Remove unnecessary whitespace from text."""
    if not value:
        return ""

    return re.sub(r"\s+", " ", value).strip()


def normalize_url(url: str) -> str:
    """Normalize a URL for consistent comparison."""
    parsed = urlparse(url.strip())

    normalized = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=parsed.netloc.lower(),
        path=parsed.path.rstrip("/"),
        fragment="",
    )

    return urlunparse(normalized)


def truncate_text(
    text: str,
    max_length: int = 500,
) -> str:
    """Limit text length without cutting off a word."""
    text = clean_text(text)

    if len(text) <= max_length:
        return text

    truncated = text[:max_length].rsplit(" ", 1)[0]
    return truncated + "..."


def extract_domain(url: str) -> str:
    """Extract the domain name from a URL."""
    return urlparse(url).netloc.lower().removeprefix("www.")
