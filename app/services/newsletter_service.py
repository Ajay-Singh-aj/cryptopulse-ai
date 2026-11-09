
from uuid import uuid4

from app.config import get_settings
from app.schemas.article import Article, ArticleCategory
from app.schemas.newsletter import Newsletter, NewsletterSection


SECTION_TITLES = {
    ArticleCategory.CRYPTOGRAPHY: "Cryptography & Research",
    ArticleCategory.PAYMENT_SECURITY: "Payment Security",
    ArticleCategory.FINTECH_REGULATION: "Fintech & Regulation",
    ArticleCategory.CYBERSECURITY: "Cybersecurity Alerts",
}


def create_newsletter(
    articles: list[Article],
    introduction: str | None = None,
) -> Newsletter:
    """Create a newsletter containing the highest-scoring articles."""

    settings = get_settings()

    # Select the highest-scoring articles first.
    selected_articles = sorted(
        articles,
        key=lambda article: article.relevance_score,
        reverse=True,
    )[:settings.MAX_ARTICLES_PER_NEWSLETTER]

    sections = []

    for category, title in SECTION_TITLES.items():
        category_articles = [
            article
            for article in selected_articles
            if article.category == category
        ]

        if category_articles:
            sections.append(
                NewsletterSection(
                    title=title,
                    articles=category_articles,
                )
            )

    return Newsletter(
        issue_id=str(uuid4()),
        introduction=introduction,
        sections=sections,
        total_articles=len(selected_articles),
        status="draft",
    )
