from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE_DIR = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = BASE_DIR / "templates"


def render_newsletter_html(newsletter) -> str:
    """Render a newsletter using the HTML template."""

    environment = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = environment.get_template("newsletter.html")

    return template.render(
        introduction=newsletter.introduction or "",
        freshness_note=newsletter.freshness_note or "",
        real_world_problem=newsletter.real_world_problem or "",
        fintech_impact=newsletter.fintech_impact or "",
        india_relevance=newsletter.india_relevance,
        authentication_factors=newsletter.authentication_factors,
        sections=newsletter.sections,
        key_takeaways=newsletter.key_takeaways,
        key_findings=newsletter.key_findings,
        why_read=newsletter.why_read or "",
        technical_flow_title=newsletter.technical_flow_title or "",
        technical_flow_steps=newsletter.technical_flow_steps,
        context_sources=newsletter.context_sources,
        issue_date=newsletter.issue_date,
        title=newsletter.title,
        total_articles=newsletter.total_articles,
    )
