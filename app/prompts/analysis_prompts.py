
from app.schemas.article import Article
from app.services.llm_service import get_llm
from app.prompts.analysis_prompts import ANALYSIS_PROMPT


def analyze_article(article: Article) -> Article:
    """Analyze an article using the configured LLM."""

    llm = get_llm()

    content = article.description or article.title

    prompt = ANALYSIS_PROMPT.format(
        title=article.title,
        source=article.source_name,
        content=content,
    )

    response = llm.invoke(prompt)
    output = response.content

    if not isinstance(output, str):
        raise ValueError("LLM returned an unexpected response format.")

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
    """Analyze multiple articles."""

    analyzed_articles = []

    for article in articles:
        try:
            analyzed_articles.append(analyze_article(article))
        except Exception:
            analyzed_articles.append(article)

    return analyzed_articles
