
import json
from datetime import datetime, timezone

from app.database.connection import get_connection
from app.schemas.newsletter import Newsletter
from app.schemas.subscriber import Subscriber


def add_subscriber(subscriber: Subscriber) -> int:
    """Add a new subscriber to the database."""

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO subscribers (
                email,
                name,
                is_active,
                preferred_topics,
                receive_research_papers,
                receive_industry_news,
                subscribed_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(subscriber.email),
                subscriber.name,
                int(subscriber.is_active),
                json.dumps(subscriber.preferred_topics),
                int(subscriber.receive_research_papers),
                int(subscriber.receive_industry_news),
                subscriber.subscribed_at.isoformat(),
            ),
        )

        return cursor.lastrowid


def get_active_subscribers() -> list[dict]:
    """Retrieve all active subscribers."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM subscribers
            WHERE is_active = 1
            ORDER BY id
            """
        ).fetchall()

        return [dict(row) for row in rows]


def save_newsletter(
    newsletter: Newsletter,
    html_content: str | None = None,
) -> int:
    """Save a generated newsletter."""

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO newsletters (
                issue_id,
                title,
                issue_date,
                generated_at,
                introduction,
                total_articles,
                status,
                html_content
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                newsletter.issue_id,
                newsletter.title,
                newsletter.issue_date.isoformat(),
                newsletter.generated_at.isoformat(),
                newsletter.introduction,
                newsletter.total_articles,
                newsletter.status,
                html_content,
            ),
        )

        return cursor.lastrowid


def record_delivery(
    newsletter_id: int,
    subscriber_id: int,
    status: str,
    error_message: str | None = None,
) -> None:
    """Record the delivery result for a subscriber."""

    if status not in {"pending", "sent", "failed"}:
        raise ValueError("Invalid delivery status.")

    sent_at = (
        datetime.now(timezone.utc).isoformat()
        if status == "sent"
        else None
    )

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO newsletter_deliveries (
                newsletter_id,
                subscriber_id,
                sent_at,
                status,
                error_message
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(newsletter_id, subscriber_id)
            DO UPDATE SET
                sent_at = excluded.sent_at,
                status = excluded.status,
                error_message = excluded.error_message
            """,
            (
                newsletter_id,
                subscriber_id,
                sent_at,
                status,
                error_message,
            ),
        )
