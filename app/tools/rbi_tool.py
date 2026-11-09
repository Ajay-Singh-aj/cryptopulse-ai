
import feedparser

RBI_FEEDS = {
    "notifications": "https://www.rbi.org.in/notifications_rss.xml",
    "press_releases": "https://www.rbi.org.in/pressreleases_rss.xml",
}


def search_rbi(
    max_results: int = 10,
    feed_type: str = "notifications",
) -> list[dict]:
    """Retrieve official RBI notifications or press releases."""

    if feed_type not in RBI_FEEDS:
        raise ValueError(
            "feed_type must be 'notifications' or 'press_releases'"
        )

    feed = feedparser.parse(RBI_FEEDS[feed_type])

    if feed.bozo and not feed.entries:
        raise RuntimeError("Unable to retrieve RBI RSS feed")

    results = []

    for entry in feed.entries[:max_results]:
        results.append({
            "title": entry.get("title", "Untitled"),
            "url": entry.get("link", ""),
            "source_name": "Reserve Bank of India",
            "source_type": "official_announcement",
            "description": entry.get("summary", ""),
            "published_at": entry.get("published"),
        })

    return results
