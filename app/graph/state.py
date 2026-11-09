
from typing import TypedDict

from app.schemas.article import Article
from app.schemas.newsletter import Newsletter


class CryptoPulseState(TypedDict, total=False):
    """Shared state for the CryptoPulse AI workflow."""

    execution_id: str

    # Research
    raw_results: list[dict]
    articles: list[Article]
    research_errors: list[str]

    # Processing
    relevant_articles: list[Article]
    verified_articles: list[Article]
    analyzed_articles: list[Article]

    # Newsletter
    newsletter: Newsletter

    # Workflow tracking
    errors: list[str]
