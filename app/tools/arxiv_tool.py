
import arxiv

from app.config import get_settings


def get_arxiv_client() -> arxiv.Client:
    """Create an arXiv API client."""

    return arxiv.Client(
        page_size=100,
        delay_seconds=3,
        num_retries=3,
    )


def search_arxiv(query: str, max_results: int | None = None) -> list[dict]:
    """
    Search arXiv and return normalized research paper metadata.
    """

    settings = get_settings()

    client = get_arxiv_client()

    search = arxiv.Search(
        query=query,
        max_results=max_results or settings.TAVILY_MAX_RESULTS,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    papers = []

    for result in client.results(search):
        papers.append({
            "title": result.title,
            "url": result.entry_id,
            "source_name": "arXiv",
            "authors": [author.name for author in result.authors],
            "description": result.summary,
            "published_at": result.published,
            "categories": result.categories,
            "primary_category": result.primary_category,
        })

    return papers
