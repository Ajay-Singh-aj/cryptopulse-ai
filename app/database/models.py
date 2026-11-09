
import sqlite3


def create_tables(connection: sqlite3.Connection) -> None:
    """Create the CryptoPulse AI database tables."""

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            name TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            preferred_topics TEXT DEFAULT '[]',
            receive_research_papers INTEGER NOT NULL DEFAULT 1,
            receive_industry_news INTEGER NOT NULL DEFAULT 1,
            subscribed_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS newsletters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_id TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            generated_at TEXT NOT NULL,
            introduction TEXT,
            total_articles INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'draft',
            html_content TEXT
        );

        CREATE TABLE IF NOT EXISTS newsletter_deliveries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newsletter_id INTEGER NOT NULL,
            subscriber_id INTEGER NOT NULL,
            sent_at TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            error_message TEXT,
            FOREIGN KEY (newsletter_id) REFERENCES newsletters(id),
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
            UNIQUE (newsletter_id, subscriber_id)
        );

        CREATE INDEX IF NOT EXISTS idx_subscribers_active
        ON subscribers(is_active);

        CREATE INDEX IF NOT EXISTS idx_newsletters_issue_date
        ON newsletters(issue_date);
        """
    )

    connection.commit()
