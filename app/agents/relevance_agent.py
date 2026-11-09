
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
        title=article.title,
        description=article.description or "",
        source=article.source_name,
    )

    response = get_llm().invoke(prompt)
    output = response.content

    if not isinstance(output, str):
        raise ValueError("Unexpected LLM response format.")

    # Extract JSON if the model wraps it in Markdown fences.
    output = output.strip().removeprefix("```json").removesuffix("```").strip()

    result = json.loads(output)

    score = max(0, min(100, int(result["relevance_score"])))

    category_value = result["category"]
    category = ArticleCategory(category_value)

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

    # Second stage: AI-based relevance evaluation.
    relevant_articles = []

    for article in candidates:
        try:
            evaluated = evaluate_relevance(article)

            if evaluated.relevance_score >= settings.MIN_RELEVANCE_SCORE:
                relevant_articles.append(evaluated)

        except Exception:
            # Preserve the keyword score if AI evaluation fails.
            logger.exception(
                "AI relevance evaluation failed for: %s",
                article.title,
            )

            relevant_articles.append(article)

    return sorted(
        relevant_articles,
        key=lambda item: item.relevance_score,
        reverse=True,
    )
