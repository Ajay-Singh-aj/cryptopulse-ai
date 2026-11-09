
from app.schemas.article import Article
from app.schemas.newsletter import Newsletter
from app.services.llm_service import get_llm
from app.services.newsletter_service import create_newsletter


def generate_newsletter(articles: list[Article]) -> Newsletter:
    """Generate a newsletter from analyzed articles."""

    newsletter = create_newsletter(articles)

    if not articles:
        return newsletter

    llm = get_llm()

    article_context = "\n\n".join(
        f"Title: {article.title}\n"
        f"Summary: {article.summary or article.description or 'Not available'}\n"
        f"Fintech impact: {article.fintech_impact or 'Not specified'}"
        for article in articles
    )

    prompt = f"""
You are the editor of CryptoPulse AI,
a cryptography and fintech intelligence newsletter.

Based on these articles, generate:

INTRODUCTION:
Write a concise introduction of 2-3 sentences.

KEY TAKEAWAYS:
Provide exactly 3 concise, factual bullet points.

Articles:
{article_context}

Do not invent information. Use only the supplied content.
"""

    try:
        response = llm.invoke(prompt)
        output = response.content

        introduction = output
        takeaways = []

        if "KEY TAKEAWAYS:" in output:
            parts = output.split("KEY TAKEAWAYS:", 1)
            introduction = parts[0].replace(
                "INTRODUCTION:", ""
            ).strip()

            takeaways = [
                line.strip().lstrip("-• ").strip()
                for line in parts[1].splitlines()
                if line.strip()
            ]

        return newsletter.model_copy(
            update={
                "introduction": introduction,
                "key_takeaways": takeaways,
            }
        )

    except Exception:
        return newsletter
