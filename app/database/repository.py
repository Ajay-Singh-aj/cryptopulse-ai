
import json
from datetime import datetime, timezone

from app.database.connection import get_connection
from app.schemas.newsletter import Newsletter
from app.schemas.subscriber import Subscriber


def _is_postgres(connection) -> bool:
    return connection.__class__.__module__.startswith("psycopg")


def add_subscriber(subscriber: Subscriber) -> int:
    with get_connection() as connection:
        postgres = _is_postgres(connection)

        query = """
            INSERT INTO subscribers (
                email, name, is_active, preferred_topics,
                receive_research_papers, receive_industry_news,
                subscribed_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """ if postgres else """
            INSERT INTO subscribers (
                email, name, is_active, preferred_topics,
                receive_research_papers, receive_industry_news,
                subscribed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        values = (
            str(subscriber.email),
            subscriber.name,
            subscriber.is_active,
            json.dumps(subscriber.preferred_topics),
            subscriber.receive_research_papers,
            subscriber.receive_industry_news,
            subscriber.subscribed_at.isoformat(),
        )

        if postgres:
            with connection.cursor() as cursor:
                cursor.execute(
                    query + " RETURNING id",
                    values,
                )
                return cursor.fetchone()["id"]

        cursor = connection.execute(
            query,
            tuple(int(v) if isinstance(v, bool) else v for v in values),
        )
        return cursor.lastrowid


def get_active_subscribers() -> list[dict]:
    with get_connection() as connection:
        if _is_postgres(connection):
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM subscribers WHERE is_active = TRUE ORDER BY id"
                )
                return cursor.fetchall()

        rows = connection.execute(
            "SELECT * FROM subscribers WHERE is_active = 1 ORDER BY id"
        ).fetchall()

        return [dict(row) for row in rows]


def save_newsletter(
    newsletter: Newsletter,
    html_content: str | None = None,
) -> int:
    with get_connection() as connection:
        query = """
            INSERT INTO newsletters (
                issue_id, title, issue_date, generated_at,
                introduction, total_articles, status, html_content
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            newsletter.issue_id,
            newsletter.title,
            newsletter.issue_date,
            newsletter.generated_at,
            newsletter.introduction,
            newsletter.total_articles,
            newsletter.status,
            html_content,
        )

        if _is_postgres(connection):
            with connection.cursor() as cursor:
                cursor.execute(query + " RETURNING id", values)
                return cursor.fetchone()["id"]

        sqlite_query = query.replace("%s", "?")
        cursor = connection.execute(
            sqlite_query,
            tuple(
                value.isoformat() if hasattr(value, "isoformat") else value
                for value in values
            ),
        )
        return cursor.lastrowid


def record_delivery(
    newsletter_id: int,
    subscriber_id: int,
    status: str,
    error_message: str | None = None,
) -> None:
    if status not in {"pending", "sent", "failed"}:
        raise ValueError("Invalid delivery status.")

    sent_at = (
        datetime.now(timezone.utc)
        if status == "sent"
        else None
    )

    with get_connection() as connection:
        if _is_postgres(connection):
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO newsletter_deliveries (
                        newsletter_id, subscriber_id, sent_at,
                        status, error_message
                    ) VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (newsletter_id, subscriber_id)
                    DO UPDATE SET
                        sent_at = EXCLUDED.sent_at,
                        status = EXCLUDED.status,
                        error_message = EXCLUDED.error_message
                    """,
                    (
                        newsletter_id,
                        subscriber_id,
                        sent_at,
                        status,
                        error_message,
                    ),
                )
        else:
            connection.execute(
                """
                INSERT INTO newsletter_deliveries (
                    newsletter_id, subscriber_id, sent_at,
                    status, error_message
                ) VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(newsletter_id, subscriber_id)
                DO UPDATE SET
                    sent_at = excluded.sent_at,
                    status = excluded.status,
                    error_message = excluded.error_message
                """,
                (
                    newsletter_id,
                    subscriber_id,
                    sent_at.isoformat() if sent_at else None,
                    status,
                    error_message,
                ),
            )
