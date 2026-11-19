from app.agents.newsletter_agent import generate_newsletter
from app.schemas.article import Article, ArticleCategory, SourceType


class FakeResponse:
    content = """**INTRODUCTION:**
A new authentication choice can change how customers approve digital payments.

**FRESHNESS / CURRENT STATUS:**
The RBI Directions were issued on 25 September 2025 and compliance was due by 1 April 2026. NPCI's UPI circular is dated 7 October 2025; biometric use is optional and depends on bank/app implementation.

**REAL-WORLD PROBLEM:**
A customer making a merchant payment can be exposed to credential theft or social engineering. Stronger, independent authentication can reduce reliance on a single compromised credential.

**INDIA / NPCI PRODUCT RELEVANCE:**
- UPI: NPCI OC-226 describes an optional on-device biometric alternative to the UPI PIN for eligible transactions, initially up to Rs 5,000.
- UPI Lite and mandate execution are stated exceptions to the PIN-authentication description in the circular.

**KEY SUMMARY:**
- RBI requires at least two distinct factors for covered domestic digital payments, subject to exemptions.
- At least one factor must be dynamic for transactions other than card-present transactions.

**KEY FINDINGS:**
- What you know includes a PIN or password.
- What you have can include a card or security token.
- What you are can include a fingerprint or face biometric.

**AUTHENTICATION FACTORS:**
- WHAT YOU KNOW — UPI PIN: a secret the customer knows.
- WHAT YOU HAVE — a card, token or OTP channel, where the scheme validates possession.
- WHAT YOU ARE — fingerprint or face biometric.
- The framework does not require all three classes in every transaction.

**FINTECH IMPACT:**
Banks and UPI apps need to validate supported methods, customer consent and implementation scope rather than assume universal biometric availability.

**TECHNICAL FLOW TITLE:**
A simplified UPI authentication choice

**TECHNICAL FLOW STEPS:**
- Customer: initiates a UPI payment in the selected app.
- App and issuer: check eligibility, device/security conditions and customer consent for an enabled method.
- Customer: authenticates using the available permitted method.
- Issuer: validates the credential and processes the authorisation decision.

**WHY YOU SHOULD READ THIS:**
Product, security and compliance teams can see which UPI journeys may change and where optional biometric authentication differs from a mandatory factor.
"""


class FakeLLM:
    def invoke(self, prompt):
        assert "VERIFIED INDIA DIGITAL-PAYMENT AUTHENTICATION CONTEXT" in prompt
        assert "do not present an old circular or announcement as breaking news" in prompt
        assert "Unselected quantum article" not in prompt
        return FakeResponse()


def test_generate_newsletter_creates_topic_specific_context_and_flow(monkeypatch):
    """Topic-aware analysis includes real-world, RBI/NPCI, factor and flow detail."""

    monkeypatch.setattr(
        "app.agents.newsletter_agent.get_llm",
        lambda: FakeLLM(),
    )

    article = Article(
        title="RBI and NPCI UPI Authentication Methods",
        url="https://example.com/upi-authentication",
        relevance_score=95,
        source_name="Reserve Bank of India",
        source_type=SourceType.OFFICIAL_ANNOUNCEMENT,
        category=ArticleCategory.PAYMENT_SECURITY,
        description="RBI two-factor authentication and UPI PIN biometric methods.",
        summary="New developments in digital payment authentication.",
        fintech_impact="Banks must support secure customer authentication.",
        metadata={
            "current_context": [{
                "title": "Official NPCI context",
                "url": "https://www.npci.org.in/product/UPI",
                "content": "UPI product reference",
            }]
        },
    )

    secondary_article = Article(
        title="Unselected quantum article",
        url="https://example.com/quantum",
        source_name="Example Research",
        source_type=SourceType.RESEARCH_PAPER,
        category=ArticleCategory.CRYPTOGRAPHY,
        description="A separate quantum cryptography topic.",
        relevance_score=60,
    )

    newsletter = generate_newsletter([secondary_article, article])

    assert "merchant payment" in newsletter.real_world_problem
    assert any("UPI:" in item for item in newsletter.india_relevance)
    assert len(newsletter.authentication_factors) == 4
    assert len(newsletter.key_takeaways) == 2
    assert len(newsletter.key_findings) == 3
    assert "Banks and UPI apps" in newsletter.fintech_impact
    assert newsletter.technical_flow_title == "A simplified UPI authentication choice"
    assert len(newsletter.technical_flow_steps) == 4
    assert "optional" in newsletter.freshness_note
    assert newsletter.why_read
    assert any("RBI Authentication" in ref.label for ref in newsletter.context_sources)
    assert any("NPCI UPI Operating Circular 226" in ref.label for ref in newsletter.context_sources)


def test_generate_newsletter_returns_empty_briefing_without_articles():
    newsletter = generate_newsletter([])
    assert newsletter.total_articles == 0
    assert newsletter.technical_flow_steps == []
