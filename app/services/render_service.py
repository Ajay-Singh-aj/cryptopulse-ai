
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
        sections=newsletter.sections,
        key_takeaways=newsletter.key_takeaways,
        issue_date=newsletter.issue_date,
        title=newsletter.title,
        total_articles=newsletter.total_articles,
    )
