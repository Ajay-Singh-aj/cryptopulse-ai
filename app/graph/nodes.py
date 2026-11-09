
from app.agents.research_agent import run_research
from app.agents.relevance_agent import filter_relevant_articles
from app.agents.verification_agent import verify_articles
from app.agents.analysis_agent import analyze_articles
from app.agents.newsletter_agent import generate_newsletter

from app.schemas.article import Article, ArticleCategory, SourceType


def _normalize_article(raw: dict) -> Article | None:
    """Convert source results into our standard Article schema."""

    title = raw.get("title")
    url = raw.get("url")

    if not title or not url:
        return None

    text = " ".join([
        str(title),
        str(raw.get("description") or raw.get("content") or ""),
    ]).lower()

    if any(term in text for term in [
        "upi", "payment security", "payment tokenization",
        "transaction security",
    ]):
        category = ArticleCategory.PAYMENT_SECURITY
    elif any(term in text for term in [
        "rbi", "npci", "fintech", "digital payment", "regulation",
    ]):
        category = ArticleCategory.FINTECH_REGULATION
    elif any(term in text for term in [
        "vulnerability", "cybersecurity", "security advisory",
        "data breach", "cyber resilience",
    ]):
        category = ArticleCategory.CYBERSECURITY
    else:
        category = ArticleCategory.CRYPTOGRAPHY

    source_name = raw.get("source_name") or raw.get("source") or "Web"

    source_type_value = raw.get("source_type")
    if source_type_value not in [item.value for item in SourceType]:
        if "arxiv" in str(source_name).lower():
            source_type_value = SourceType.RESEARCH_PAPER.value
        elif "cert-in" in str(source_name).lower():
            source_type_value = SourceType.SECURITY_ADVISORY.value
        elif str(source_name).lower() in ["nist", "npci", "reserve bank of india"]:
            source_type_value = SourceType.OFFICIAL_ANNOUNCEMENT.value
        else:
            source_type_value = SourceType.WEB.value

    try:
        return Article(
            title=str(title),
            url=url,
            source_name=str(source_name),
            source_type=source_type_value,
            category=category,
            description=raw.get("description") or raw.get("content"),
            authors=raw.get("authors") or [],
            published_at=raw.get("published_at"),
            keywords=raw.get("keywords") or [],
            metadata=raw,
        )
    except Exception:
        return None


def research_node(state: dict) -> dict:
    """Collect and normalize research results."""

    result = run_research()

    articles = [
        article
        for raw in result["results"]
        if (article := _normalize_article(raw)) is not None
    ]

    return {
        "execution_id": result["execution_id"],
        "articles": articles,
        "research_errors": result["errors"],
    }


def relevance_node(state: dict) -> dict:
    """Filter articles by relevance."""

    articles = filter_relevant_articles(state.get("articles", []))

    return {"relevant_articles": articles}


def verification_node(state: dict) -> dict:
    """Verify original article URLs."""

    articles = verify_articles(state.get("relevant_articles", []))

    return {"verified_articles": articles}


def analysis_node(state: dict) -> dict:
    """Analyze verified articles."""

    articles = [
        article
        for article in state.get("verified_articles", [])
        if article.verified
    ]

    analyzed = analyze_articles(articles)

    return {"analyzed_articles": analyzed}


def newsletter_node(state: dict) -> dict:
    """Generate the final newsletter draft."""

    newsletter = generate_newsletter(
        state.get("analyzed_articles", [])
    )

    return {"newsletter": newsletter}
