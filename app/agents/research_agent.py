
from uuid import uuid4

from app.tools.tavily_tool import get_tavily_tool
from app.tools.arxiv_tool import search_arxiv
from app.tools.certin_tool import search_certin
from app.tools.nist_tool import search_nist
from app.tools.rbi_tool import search_rbi


def run_research() -> dict:
    """Collect research articles and announcements from configured sources."""

    execution_id = str(uuid4())
    results = []
    errors = []

    # Tavily web research
    try:
        tavily = get_tavily_tool()
        response = tavily.invoke({
            "query": (
                "Latest cryptography, post-quantum cryptography, "
                "UPI payment security and fintech developments"
            )
        })

        if isinstance(response, dict):
            results.extend(response.get("results", []))

    except Exception as exc:
        errors.append(f"Tavily: {exc}")

    # arXiv research papers
    try:
        results.extend(
            search_arxiv("all:post-quantum cryptography", max_results=5)
        )
    except Exception as exc:
        errors.append(f"arXiv: {exc}")

    # CERT-In advisories
    try:
        results.extend(search_certin(max_results=5))
    except Exception as exc:
        errors.append(f"CERT-In: {exc}")

    # NIST PQC updates
    try:
        results.extend(search_nist(max_results=5))
    except Exception as exc:
        errors.append(f"NIST: {exc}")

    # RBI notifications
    try:
        results.extend(search_rbi(max_results=5))
    except Exception as exc:
        errors.append(f"RBI: {exc}")

    return {
        "execution_id": execution_id,
        "total_results": len(results),
        "results": results,
        "errors": errors,
    }
