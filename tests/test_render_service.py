from app.schemas.article import Article, ArticleCategory, SourceType
from app.services.newsletter_service import create_newsletter
from app.services.render_service import render_newsletter_html


def test_render_newsletter_html():
    """Test rendering a readable newsletter with article analysis sections."""

    article = Article(
        title="Post-Quantum Cryptography Developments",
        url="https://example.com/pqc",
        source_name="Example Research",
        source_type=SourceType.RESEARCH_PAPER,
        category=ArticleCategory.CRYPTOGRAPHY,
        description="An update about quantum-resistant cryptography.",
        summary="New developments in post-quantum cryptography.",
        fintech_impact=(
            "Financial institutions should prepare for quantum-resistant security."
        ),
    )

    newsletter = create_newsletter(
        articles=[article],
        introduction="Welcome to CryptoPulse AI!",
    )
    newsletter.key_takeaways = [
        "Post-quantum cryptography is evolving.",
        "Financial institutions need stronger security.",
    ]
    newsletter.key_findings = [
        "Researchers reported progress on quantum-resistant algorithms.",
        "Financial institutions face migration work ahead.",
    ]
    newsletter.why_read = (
        "This article helps security and fintech teams understand "
        "why post-quantum readiness matters."
    )

    html = render_newsletter_html(newsletter)

    assert isinstance(html, str)
    assert len(html) > 100
    assert "CryptoPulse AI" in html
    assert "Post-Quantum Cryptography Developments" in html
    assert "Welcome to CryptoPulse AI!" in html
    assert "Key Summary" in html
    assert "Key Findings" in html
    assert "Why You Should Read This" in html
    assert "quantum-resistant algorithms" in html
    assert "post-quantum readiness matters" in html
