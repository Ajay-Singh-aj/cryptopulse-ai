from app.schemas.article import Article, ArticleCategory, SourceType
from app.schemas.newsletter import NewsletterReference
from app.services.newsletter_service import create_newsletter
from app.services.render_service import render_newsletter_html


def test_render_newsletter_html():
    """Render topic-aware analysis blocks and an email-safe process flow."""

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
        introduction="Welcome to CryptoPulse AI!",
    )
    newsletter.freshness_note = "The paper is historical background; a later standard is in effect."
    newsletter.real_world_problem = (
        "Financial institutions need to migrate long-lived data and systems "
        "before quantum-capable attackers can exploit it."
    )
    newsletter.fintech_impact = "Banks should inventory cryptographic dependencies."
    newsletter.india_relevance = [
        "No direct NPCI product impact is established by the source."
    ]
    newsletter.authentication_factors = [
        "WHAT YOU KNOW — a PIN or password.",
        "WHAT YOU HAVE — a hardware or software token.",
        "WHAT YOU ARE — a fingerprint or face biometric.",
    ]
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
    newsletter.technical_flow_title = "A simplified key-establishment flow"
    newsletter.technical_flow_steps = [
        "Client: requests a secure session.",
        "Server: presents its cryptographic identity.",
        "Client and server: establish shared session keys.",
    ]
    newsletter.context_sources = [
        NewsletterReference(
            label="NIST Post-Quantum Cryptography",
            url="https://www.nist.gov/pqcrypto",
        )
    ]

    html = render_newsletter_html(newsletter)

    assert isinstance(html, str)
    assert len(html) > 100
    assert "CryptoPulse AI" in html
    assert "Post-Quantum Cryptography Developments" in html
    assert "Welcome to CryptoPulse AI!" in html
    assert "Freshness &amp; Current Status" in html
    assert "The Real-World Problem" in html
    assert "India / NPCI Product Relevance" in html
    assert "Key Summary" in html
    assert "Key Findings" in html
    assert "Authentication: What You Know, Have &amp; Are" in html
    assert "FinTech Impact" in html
    assert "A simplified key-establishment flow" in html
    assert "Why You Should Read This" in html
    assert "Official Context &amp; References" in html
    assert "nist.gov/pqcrypto" in html
