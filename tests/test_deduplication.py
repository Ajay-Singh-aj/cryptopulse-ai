
from app.schemas.article import Article
from app.services.deduplication_service import deduplicate_articles


def test_duplicate_urls_are_removed():
    article_data = {
        "title": "Post-Quantum Cryptography Research",
        "source_name": "Test Source",
        "source_type": "research_paper",
        "category": "cryptography",
    }

    articles = [
        Article(
            **article_data,
            url="https://example.com/research",
        ),
        Article(
            **article_data,
            url="https://example.com/research/",
        ),
        Article(
            **article_data,
            url="https://example.com/another-paper",
        ),
    ]

    results = deduplicate_articles(articles)

    assert len(results) == 2
    assert str(results[0].url).rstrip("/") == (
        "https://example.com/research"
    )
    assert str(results[1].url).rstrip("/") == (
        "https://example.com/another-paper"
    )
