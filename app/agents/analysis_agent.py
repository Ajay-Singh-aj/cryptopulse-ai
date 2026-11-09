
from app.schemas.article import Article
from app.services.llm_service import get_llm


def analyze_article(article: Article) -> Article:
    """Generate an AI-powered summary and fintech impact analysis."""

    llm = get_llm()

    content = article.description or article.title

    prompt = f"""
You are a cryptography and fintech research analyst.

Analyze this article for a technical fintech newsletter.

Title: {article.title}
Source: {article.source_name}
Description:
{content}

Provide two sections:

SUMMARY:
Write a concise summary in 3-5 sentences.

FINTECH IMPACT:
Explain the practical implications for payment systems,
banking, cryptography, or financial cybersecurity.
If there is no direct fintech impact, state that clearly.

Use only the information provided. Do not invent facts.
"""

    response = llm.invoke(prompt)
    output = response.content

    summary = output
    fintech_impact = None

    if "FINTECH IMPACT:" in output:
        parts = output.split("FINTECH IMPACT:", 1)
        summary = parts[0].replace("SUMMARY:", "").strip()
        fintech_impact = parts[1].strip()

    return article.model_copy(
        update={
            "summary": summary,
            "fintech_impact": fintech_impact,
        }
    )


def analyze_articles(articles: list[Article]) -> list[Article]:
    """Analyze a collection of articles."""

    analyzed_articles = []

    for article in articles:
        try:
            analyzed_articles.append(analyze_article(article))
        except Exception:
            # Preserve the article if AI analysis fails.
            analyzed_articles.append(article)

    return analyzed_articles
