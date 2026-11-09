
from app.agents import research_agent


class MockTavily:
    """Mock Tavily search tool for testing."""

    def invoke(self, input_data):
        return {
            "results": [
                {
                    "title": "Post-Quantum Cryptography Developments",
                    "url": "https://example.com/cryptography",
                    "content": "Important cryptography research update.",
                    "source": "Example Research",
                }
            ]
        }


def test_run_research(monkeypatch):
    """Test research collection without external API calls."""

    # Mock AI query generation.
    monkeypatch.setattr(
        research_agent,
        "generate_research_queries",
        lambda: ["test cryptography query"],
    )

    # Mock Tavily.
    monkeypatch.setattr(
        research_agent,
        "get_tavily_tool",
        lambda: MockTavily(),
    )

    # Mock all external research sources.
    monkeypatch.setattr(
        research_agent,
        "search_arxiv",
        lambda *args, **kwargs: [],
    )

    monkeypatch.setattr(
        research_agent,
        "search_certin",
        lambda **kwargs: [],
    )

    monkeypatch.setattr(
        research_agent,
        "search_nist",
        lambda **kwargs: [],
    )

    monkeypatch.setattr(
        research_agent,
        "search_rbi",
        lambda **kwargs: [],
    )

    # Execute research.
    result = research_agent.run_research()

    # Verify output.
    assert result["execution_id"]
    assert result["total_results"] == 1
    assert len(result["results"]) == 1
    assert result["errors"] == []
    assert (
        result["results"][0]["title"]
        == "Post-Quantum Cryptography Developments"
    )
