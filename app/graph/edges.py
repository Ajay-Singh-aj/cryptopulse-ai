
from langgraph.graph import END


def should_continue_after_research(state: dict) -> str:
    """Check whether research produced usable articles."""

    if state.get("articles"):
        return "relevance"

    return END


def should_continue_after_verification(state: dict) -> str:
    """Continue only if at least one article is verified."""

    verified_articles = [
        article
        for article in state.get("verified_articles", [])
        if article.verified
    ]

    if verified_articles:
        return "analysis"

    return END
