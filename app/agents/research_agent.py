
import json
import logging
from uuid import uuid4

from app.services.llm_service import get_llm
from app.prompts.research_prompts import RESEARCH_PROMPT
from app.utils.date_utils import get_current_date

from app.tools.tavily_tool import get_tavily_tool
from app.tools.arxiv_tool import search_arxiv
from app.tools.certin_tool import search_certin
from app.tools.nist_tool import search_nist
from app.tools.rbi_tool import search_rbi

logger = logging.getLogger(__name__)

RESEARCH_TOPICS = [
    "Post-quantum cryptography and cryptographic research",
    "UPI and digital payment security in India",
    "RBI and fintech regulatory developments",
    "Financial cybersecurity and security vulnerabilities",
]


def generate_research_queries() -> list[str]:
    """Generate focused research queries using Groq."""

    prompt = RESEARCH_PROMPT.format(
        topic=", ".join(RESEARCH_TOPICS),
        current_date=get_current_date().isoformat(),
        max_queries=5,
    )

    response = get_llm().invoke(prompt)
    output = response.content

    if not isinstance(output, str):
        raise ValueError("Unexpected LLM response format.")

    output = (
        output.strip()
        .removeprefix("```json")
        .removesuffix("```")
        .strip()
    )

    result = json.loads(output)
    queries = result.get("queries", [])

    if not isinstance(queries, list):
        raise ValueError("Research queries must be a list.")

    return [
        query.strip()
        for query in queries
        if isinstance(query, str) and query.strip()
    ][:5]


def run_research() -> dict:
    """Collect research from configured sources."""

    execution_id = str(uuid4())
    results = []
    errors = []

    try:
        queries = generate_research_queries()
    except Exception as exc:
        logger.exception("AI query generation failed.")
        errors.append(f"Query generation: {exc}")

        queries = [
            "Latest cryptography and post-quantum cryptography developments",
            "UPI payment security and Indian fintech developments",
            "Latest RBI fintech cybersecurity announcements",
        ]

    try:
        tavily = get_tavily_tool()

        for query in queries:
            try:
                response = tavily.invoke({"query": query})

                if isinstance(response, dict):
                    results.extend(response.get("results", []))

            except Exception as exc:
                errors.append(f"Tavily ({query}): {exc}")

    except Exception as exc:
        errors.append(f"Tavily initialization: {exc}")

    sources = [
        ("arXiv", lambda: search_arxiv(
            "all:post-quantum cryptography", max_results=5
        )),
        ("CERT-In", lambda: search_certin(max_results=5)),
        ("NIST", lambda: search_nist(max_results=5)),
        ("RBI", lambda: search_rbi(max_results=5)),
    ]

    for source_name, search_function in sources:
        try:
            results.extend(search_function())
        except Exception as exc:
            errors.append(f"{source_name}: {exc}")

    return {
        "execution_id": execution_id,
        "total_results": len(results),
        "results": results,
        "errors": errors,
    }
