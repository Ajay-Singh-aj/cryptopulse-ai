
from app.config import get_settings
from app.schemas.article import Article
from app.services.scoring_service import score_articles


def filter_relevant_articles(
    articles: list[Article],
) -> list[Article]:
    """Score articles and retain only relevant ones."""

    settings = get_settings()

    scored_articles = score_articles(articles)

    relevant_articles = [
        article
        for article in scored_articles
        if article.relevance_score >= settings.MIN_RELEVANCE_SCORE
    ]

    return relevant_articles
