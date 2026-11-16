from app.agents.newsletter_agent import generate_newsletter
from app.schemas.article import Article, ArticleCategory, SourceType


class FakeResponse:
    content = """**INTRODUCTION:**
This development matters to teams preparing for post-quantum security.

**KEY SUMMARY:**
- Researchers reported progress on quantum-resistant algorithms.
- Financial institutions should begin assessing migration readiness.

**KEY FINDINGS:**
- The work concerns post-quantum cryptography.
- The supplied summary identifies preparation as a financial-sector concern.

**WHY YOU SHOULD READ THIS:**
Security and fintech readers can use this context to understand why
post-quantum planning deserves attention.
"""


class FakeLLM:
    def invoke(self, prompt):
        return FakeResponse()


def test_generate_newsletter_parses_structured_article_sections(monkeypatch):
    """Generated headings and bullets populate the newsletter fields."""

    monkeypatch.setattr(
        "app.agents.newsletter_agent.get_llm",
        lambda: FakeLLM(),
    )

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

    newsletter = generate_newsletter([article])

    assert "This development matters" in newsletter.introduction
    assert len(newsletter.key_takeaways) == 2
    assert "quantum-resistant algorithms" in newsletter.key_takeaways[0]
    assert len(newsletter.key_findings) == 2
    assert newsletter.why_read is not None
    assert "post-quantum planning" in newsletter.why_read
