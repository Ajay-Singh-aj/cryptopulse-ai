
from app.schemas.article import Article
from app.schemas.newsletter import Newsletter
from app.services.llm_service import get_llm
from app.services.newsletter_service import create_newsletter
from app.prompts.newsletter_prompts import NEWSLETTER_PROMPT


def generate_newsletter(articles: list[Article]) -> Newsletter:
    """Generate a newsletter using analyzed articles."""

    newsletter = create_newsletter(articles)

    if not articles:
        return newsletter

    article_context = "\n\n".join(
        f"""
Title: {article.title}
Source: {article.source_name}
Summary: {article.summary or article.description or 'Not available'}
Fintech impact: {article.fintech_impact or 'Not specified'}
"""
        for article in articles
    )

    prompt = NEWSLETTER_PROMPT.format(
        articles=article_context
    )

    try:
        llm = get_llm()
        response = llm.invoke(prompt)
        output = response.content

        if not isinstance(output, str):
            raise ValueError("Unexpected LLM response format.")

        introduction = output
        takeaways = []

        if "KEY TAKEAWAYS:" in output:
            parts = output.split("KEY TAKEAWAYS:", 1)

            introduction = (
                parts[0]
                .replace("INTRODUCTION:", "")
                .strip()
            )

            takeaways = [
                line.strip().lstrip("-• ").strip()
                for line in parts[1].splitlines()
                if line.strip()
            ]

        return newsletter.model_copy(
            update={
                "introduction": introduction,
                "key_takeaways": takeaways[:3],
            }
        )

    except Exception:
        return newsletter
