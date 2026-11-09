
from app.agents import research_agent


class MockTavily:
    def invoke(self, query):
        return {
            "results": [
                {
                    "title": "Post-Quantum Cryptography Update",
                    "url": "https://example.com/pqc",
                    "source_name": "Tavily",
                }
            ]
        }


def test_run_research(monkeypatch):
    monkeypatch.setattr(
        research_agent,
        "get_tavily_tool",
        lambda: MockTavily(),
    )
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

    result = research_agent.run_research()

    assert result["execution_id"]
    assert result["total_results"] == 1
    assert len(result["results"]) == 1
    assert result["errors"] == []
