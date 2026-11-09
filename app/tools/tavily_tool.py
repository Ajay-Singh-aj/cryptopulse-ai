
from langchain_tavily import TavilySearch

from app.config import get_settings


def get_tavily_tool() -> TavilySearch:
    """
    Create and return the Tavily search tool.
    """

    settings = get_settings()

    if not settings.TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY is missing from .env")

    return TavilySearch(
        max_results=settings.TAVILY_MAX_RESULTS,
        topic="general",
        search_depth=settings.TAVILY_SEARCH_DEPTH,
        tavily_api_key=settings.TAVILY_API_KEY.get_secret_value(),
    )
