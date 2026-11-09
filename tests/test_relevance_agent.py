
from app.agents.relevance_agent import filter_relevant_articles
from app.schemas.article import Article, ArticleCategory, SourceType


def test_filter_relevant_articles():
    articles = [
        Article(
            title="Post Quantum Cryptography in Payment Systems",
            url="https://example.com/pqc",
            source_name="Test",
            source_type=SourceType.WEB,
            category=ArticleCategory.CRYPTOGRAPHY,
            description="Research on post-quantum cryptography.",
        ),
        Article(
            title="General Technology News",
            url="https://example.com/general",
            source_name="Test",
            source_type=SourceType.WEB,
            category=ArticleCategory.CYBERSECURITY,
            description="An unrelated general technology update.",
        ),
    ]

    results = filter_relevant_articles(articles)

    assert all(
        article.relevance_score >= 60
        for article in results
    )
