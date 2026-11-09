
import json
import logging

from app.schemas.article import Article
from app.tools.web_content_tool import fetch_web_content
from app.services.llm_service import get_llm
from app.prompts.verification_prompts import VERIFICATION_PROMPT

logger = logging.getLogger(__name__)


def verify_article(article: Article) -> Article:
    """Verify an article using its webpage and AI assessment."""

    try:
        page = fetch_web_content(str(article.url))
        content = page.get("content", "").strip()

        if len(content) < 100:
            return article.model_copy(
                update={"verified": False}
            )

        prompt = VERIFICATION_PROMPT.format(
            title=article.title,
            url=str(article.url),
            source=article.source_name,
            content=content[:10000],
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

        is_verified = (
            result.get("verified") is True
            and int(result.get("credibility_score", 0)) >= 60
        )

        return article.model_copy(
            update={
                "verified": is_verified,
                "description": content[:5000],
                "metadata": {
                    **article.metadata,
                    "verification_reason": result.get("reason", ""),
                    "credibility_score": result.get(
                        "credibility_score", 0
                    ),
                },
            }
        )

    except Exception:
        logger.exception(
            "Article verification failed: %s",
            article.title,
        )

        return article.model_copy(
            update={"verified": False}
        )


def verify_articles(articles: list[Article]) -> list[Article]:
    """Verify a collection of articles."""

    return [
        verify_article(article)
        for article in articles
    ]
