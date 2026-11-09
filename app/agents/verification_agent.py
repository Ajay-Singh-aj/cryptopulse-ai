
from app.schemas.article import Article
from app.tools.web_content_tool import fetch_web_content


def verify_articles(articles: list[Article]) -> list[Article]:
    """Verify articles by checking their original webpage content."""

    verified_articles = []

    for article in articles:
        try:
            page = fetch_web_content(str(article.url))

            is_verified = (
                bool(page.get("content", "").strip())
                and len(page.get("content", "").strip()) >= 100
            )

            verified_articles.append(
                article.model_copy(
                    update={"verified": is_verified}
                )
            )

        except Exception:
            verified_articles.append(
                article.model_copy(update={"verified": False})
            )

    return verified_articles
