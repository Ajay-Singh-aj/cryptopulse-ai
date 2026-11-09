
import logging

from app.database.repository import (
    get_active_subscribers,
    record_delivery,
    save_newsletter,
)
from app.services.email_service import send_email
from app.services.render_service import render_newsletter_html
from app.schemas.newsletter import Newsletter

logger = logging.getLogger(__name__)


def deliver_newsletter(newsletter: Newsletter) -> dict:
    """Render and deliver a newsletter to active subscribers."""

    subscribers = get_active_subscribers()

    if not subscribers:
        logger.warning("No active subscribers found.")
        return {
            "total": 0,
            "sent": 0,
            "failed": 0,
        }

    html_content = render_newsletter_html(newsletter)

    newsletter_id = save_newsletter(
        newsletter,
        html_content=html_content,
    )

    sent = 0
    failed = 0

    for subscriber in subscribers:
        subscriber_id = subscriber["id"]
        email = subscriber["email"]

        try:
            send_email(
                subject=newsletter.title,
                html_content=html_content,
                recipients=[email],
                text_content=(
                    f"{newsletter.title}\n\n"
                    f"{newsletter.introduction or ''}"
                ),
            )

            record_delivery(
                newsletter_id=newsletter_id,
                subscriber_id=subscriber_id,
                status="sent",
            )

            sent += 1
            logger.info("Newsletter sent to %s", email)

        except Exception as exc:
            record_delivery(
                newsletter_id=newsletter_id,
                subscriber_id=subscriber_id,
                status="failed",
                error_message=str(exc),
            )

            failed += 1
            logger.exception("Delivery failed for %s", email)

    return {
        "total": len(subscribers),
        "sent": sent,
        "failed": failed,
    }
