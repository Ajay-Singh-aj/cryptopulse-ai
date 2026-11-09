
from uuid import uuid4

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
    """Organize articles into a newsletter."""

    sections = []

    for category, title in SECTION_TITLES.items():
        category_articles = [
            article
            for article in articles
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
        total_articles=sum(
            len(section.articles) for section in sections
        ),
        status="draft",
    )
