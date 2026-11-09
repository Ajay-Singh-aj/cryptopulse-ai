
from app.schemas.article import Article


def deduplicate_articles(
    articles: list[Article],
) -> list[Article]:
    """Remove duplicate articles based on their normalized URLs."""

    unique_articles = []
    seen_urls = set()

    for article in articles:
        normalized_url = str(article.url).strip().rstrip("/").lower()

        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)
        unique_articles.append(article)

    return unique_articles
