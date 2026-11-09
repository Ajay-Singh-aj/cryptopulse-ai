
import json
import logging

from app.config import get_settings
from app.schemas.article import Article, ArticleCategory
from app.services.llm_service import get_llm
from app.services.scoring_service import score_articles
from app.prompts.relevance_prompts import RELEVANCE_PROMPT

logger = logging.getLogger(__name__)


def evaluate_relevance(article: Article) -> Article:
    """Evaluate an article's relevance using the LLM."""

    prompt = RELEVANCE_PROMPT.format(
        title=article.title[:300],
        description=(article.description or "")[:1200],
        source=article.source_name[:150],
    )

    response = get_llm().invoke(
        prompt,
        config={"max_tokens": 300},
    )

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

    score = max(
        0,
        min(100, int(result["relevance_score"])),
    )

    category = ArticleCategory(result["category"])

    return article.model_copy(
        update={
            "relevance_score": score,
            "category": category,
            "metadata": {
                **article.metadata,
                "relevance_reason": result.get("reason", ""),
            },
        }
    )


def filter_relevant_articles(
    articles: list[Article],
) -> list[Article]:
    """Score articles and filter by minimum relevance."""

    settings = get_settings()

    # First stage: inexpensive keyword-based scoring.
    candidates = [
        article
        for article in score_articles(articles)
        if article.relevance_score >= settings.MIN_RELEVANCE_SCORE
    ]

    if not candidates:
        return []

    # Limit the number of AI evaluations per run.
    max_ai_evaluations = 5
    relevant_articles = []

    for index, article in enumerate(candidates):
        if index >= max_ai_evaluations:
            relevant_articles.append(article)
            continue

        try:
            evaluated = evaluate_relevance(article)

            if evaluated.relevance_score >= settings.MIN_RELEVANCE_SCORE:
                relevant_articles.append(evaluated)

        except Exception as exc:
            logger.warning(
                "AI relevance evaluation failed for %s: %s",
                article.title,
                exc,
            )

            # Preserve the keyword score if AI evaluation fails.
            relevant_articles.append(article)

    return sorted(
        relevant_articles,
        key=lambda item: item.relevance_score,
        reverse=True,
    )
