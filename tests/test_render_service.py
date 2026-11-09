
from app.schemas.article import Article, ArticleCategory, SourceType
from app.services.newsletter_service import create_newsletter
from app.services.render_service import render_newsletter_html


def test_render_newsletter_html():
    """Test rendering a newsletter into HTML."""

    article = Article(
        title="Post-Quantum Cryptography Developments",
        url="https://example.com/pqc",
        source_name="Example Research",
        source_type=SourceType.RESEARCH_PAPER,
        category=ArticleCategory.CRYPTOGRAPHY,
        description="An update about quantum-resistant cryptography.",
        summary="New developments in post-quantum cryptography.",
        fintech_impact="Financial institutions should prepare for quantum-resistant security.",
    )

    newsletter = create_newsletter(
        articles=[article],
        introduction="Welcome to CryptoPulse AI!"
    )

    newsletter.key_takeaways = [
        "Post-quantum cryptography is evolving.",
        "Financial institutions need stronger security.",
        "Cryptographic standards continue to develop.",
    ]

    html = render_newsletter_html(newsletter)

    assert isinstance(html, str)
    assert len(html) > 100
    assert "CryptoPulse AI" in html
    assert "Post-Quantum Cryptography Developments" in html
    assert "Welcome to CryptoPulse AI!" in html
