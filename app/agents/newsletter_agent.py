from app.schemas.article import Article
from app.schemas.newsletter import Newsletter
from app.services.llm_service import get_llm
from app.services.newsletter_service import create_newsletter


def _parse_bullets(text: str) -> list[str]:
    """Extract concise bullet items from a model-generated section."""
    items = []
    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned.startswith(("-", "•", "*")):
            cleaned = cleaned.lstrip("-•* ").strip()
        elif cleaned[:2].rstrip(".").isdigit():
            cleaned = cleaned[2:].lstrip(".) ").strip()
        else:
            continue
        if cleaned:
            items.append(cleaned)
    return items


def generate_newsletter(articles: list[Article]) -> Newsletter:
    """Generate an editorial briefing from analyzed articles."""

    newsletter = create_newsletter(articles)

    if not articles:
        return newsletter

    llm = get_llm()

    article_context = "\n\n".join(
        f"Title: {article.title}\n"
        f"Source: {article.source_name}\n"
        f"Summary: {article.summary or article.description or 'Not available'}\n"
        f"Fintech impact: {article.fintech_impact or 'Not specified'}"
        for article in articles
    )

    prompt = f"""
You are the editor of CryptoPulse AI, a cryptography and fintech
intelligence newsletter. Write a clear, useful editorial briefing.

Return exactly these sections, with the labels unchanged:

INTRODUCTION:
Write 2 concise sentences introducing why this development matters.

KEY SUMMARY:
Write 2-3 short bullets covering the central development and its significance.

KEY FINDINGS:
Write 3-5 factual bullets. Include concrete details, entities, dates, figures,
technical findings, or implications only when present in the source material.

WHY YOU SHOULD READ THIS:
Write 2-3 sentences explaining who should care and what practical insight,
decision, risk, or opportunity a reader can take away. Make this specific
to the article, not generic marketing copy.

Articles:
{article_context}

Rules:
- Use only the supplied information; do not invent facts, numbers, quotes,
  dates, causal claims, or predictions.
- Clearly distinguish reported facts from implications.
- Avoid repeating the same point across sections.
- Keep wording accessible and concise.
- If a requested detail is not supported, omit it rather than guessing.
"""

    try:
        response = llm.invoke(prompt)
        output = response.content or ""

        labels = [
            "INTRODUCTION:",
            "KEY SUMMARY:",
            "KEY FINDINGS:",
            "WHY YOU SHOULD READ THIS:",
        ]
        sections = {}
        current = None
        buffers = {label: [] for label in labels}

        for line in output.splitlines():
            stripped = line.strip()
            normalized_heading = stripped.strip("#*_ \\t\`").upper()
            matched = next(
                (label for label in labels if normalized_heading == label),
                None,
            )
            if matched:
                current = matched
                continue
            if current:
                buffers[current].append(line)

        for label, lines in buffers.items():
            sections[label] = "\n".join(lines).strip()

        introduction = sections["INTRODUCTION:"] or newsletter.introduction or ""
        key_summary = _parse_bullets(sections["KEY SUMMARY:"])
        key_findings = _parse_bullets(sections["KEY FINDINGS:"])
        why_read = sections["WHY YOU SHOULD READ THIS:"]

        # Keep a useful fallback if the model returns an incomplete response.
        if not key_summary:
            key_summary = [
                article.summary or article.description
                for article in articles
                if article.summary or article.description
            ][:3]
        if not key_findings:
            key_findings = [
                article.fintech_impact
                for article in articles
                if article.fintech_impact
            ][:3]
        if not why_read:
            why_read = (
                "Read the original article to understand the full context, "
                "supporting details, and implications for the relevant field."
            )

        return newsletter.model_copy(
            update={
                "introduction": introduction,
                "key_takeaways": key_summary,
                "key_findings": key_findings,
                "why_read": why_read,
            }
        )

    except Exception:
        return newsletter
