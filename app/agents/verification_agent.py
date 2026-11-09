
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
        # Fetch the original article.
        try:
            page = fetch_web_content(str(article.url))
        except Exception as exc:
            logger.warning(
                "Could not fetch article content for %s: %s",
                article.title,
                exc,
            )

            return article.model_copy(
                update={
                    "verified": False,
                    "metadata": {
                        **article.metadata,
                        "verification_reason": (
                            "Source page could not be accessed."
                        ),
                    },
                }
            )

        content = page.get("content", "").strip()

        # Reject pages without sufficient content.
        if len(content) < 100:
            logger.warning(
                "Insufficient content for verification: %s",
                article.title,
            )

            return article.model_copy(
                update={
                    "verified": False,
                    "metadata": {
                        **article.metadata,
                        "verification_reason": (
                            "Insufficient article content."
                        ),
                    },
                }
            )

        # Limit input size to control Groq token usage.
        prompt = VERIFICATION_PROMPT.format(
            title=article.title[:300],
            url=str(article.url),
            source=article.source_name[:150],
            content=content[:2500],
        )

        # Limit response tokens.
        response = get_llm().invoke(
            prompt,
            config={"max_tokens": 300},
        )

        output = response.content

        if not isinstance(output, str):
            raise ValueError("Unexpected LLM response format.")

        # Remove optional Markdown code fences.
        output = (
            output.strip()
            .removeprefix("```json")
            .removesuffix("```")
            .strip()
        )

        result = json.loads(output)

        credibility_score = int(
            result.get("credibility_score", 0)
        )

        is_verified = (
            result.get("verified") is True
            and credibility_score >= 60
        )

        return article.model_copy(
            update={
                "verified": is_verified,
                "description": content[:2500],
                "metadata": {
                    **article.metadata,
                    "verification_reason": result.get(
                        "reason",
                        "",
                    ),
                    "credibility_score": credibility_score,
                },
            }
        )

    except Exception as exc:
        logger.warning(
            "Article verification failed for %s: %s",
            article.title,
            exc,
        )

        return article.model_copy(
            update={
                "verified": False,
                "metadata": {
                    **article.metadata,
                    "verification_reason": (
                        "Verification failed due to a processing error."
                    ),
                },
            }
        )


def verify_articles(articles: list[Article]) -> list[Article]:
    """Verify a collection of articles."""

    return [
        verify_article(article)
        for article in articles
    ]
