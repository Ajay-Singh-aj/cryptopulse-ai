from app.agents.analysis_agent import (\n    _is_official_context_url,\n    analyze_articles,\n    retrieve_current_context,\n)
from app.schemas.article import Article, ArticleCategory, SourceType


def test_official_context_url_filter():
    assert _is_official_context_url("https://www.npci.org.in/product/UPI")
    assert _is_official_context_url("https://www.rbi.org.in/Scripts/NotificationUser.aspx")
    assert not _is_official_context_url("https://example.com/npci-authentication")
    assert not _is_official_context_url("https://npci.org.in.attacker.example/fake")


def test_current_context_keeps_only_official_sources(monkeypatch):
    class FakeTavily:
        def invoke(self, payload):
            assert "Latest official updates" in payload["query"]
            return {
                "results": [
                    {
                        "title": "NPCI UPI Circular",
                        "url": "https://www.npci.org.in/circulars/upi",
                        "published_date": "2026-01-01",
                        "content": "Official UPI authentication update.",
                    },
                    {
                        "title": "Unofficial commentary",
                        "url": "https://example.com/blog",
                        "content": "Unverified discussion.",
                    },
                    {
                        "title": "RBI Directions",
                        "url": "https://www.rbi.org.in/notification",
                        "content": "Official RBI direction.",
                    },
                ]
            }

    monkeypatch.setattr(
        "app.agents.analysis_agent.get_tavily_tool",
        lambda: FakeTavily(),
    )

    article = Article(
        title="RBI digital payment authentication",
        url="https://example.com/article",
        source_name="Example",
        source_type=SourceType.WEB,
        category=ArticleCategory.PAYMENT_SECURITY,
        description="Two-factor authentication for Indian payments.",
    )

    context = retrieve_current_context(article)

    assert len(context) == 2
    assert all("example.com" not in item["url"] for item in context)
    assert context[0]["title"] == "NPCI UPI Circular"



def test_only_top_ranked_article_gets_current_context_lookup(monkeypatch):
    calls = []

    def fake_analyze(article, retrieve_context=True):
        calls.append((article.title, retrieve_context))
        return article

    monkeypatch.setattr(
        "app.agents.analysis_agent.analyze_article",
        fake_analyze,
    )

    lower = Article(
        title="Lower ranked article",
        url="https://example.com/lower",
        source_name="Example",
        source_type=SourceType.WEB,
        category=ArticleCategory.CRYPTOGRAPHY,
        relevance_score=55,
    )
    lead = Article(
        title="Selected lead article",
        url="https://example.com/lead",
        source_name="Example",
        source_type=SourceType.WEB,
        category=ArticleCategory.PAYMENT_SECURITY,
        relevance_score=95,
    )

    results = analyze_articles([lower, lead])

    assert [item.title for item in results] == [
        "Selected lead article",
        "Lower ranked article",
    ]
    assert calls == [
        ("Selected lead article", True),
        ("Lower ranked article", False),
    ]
