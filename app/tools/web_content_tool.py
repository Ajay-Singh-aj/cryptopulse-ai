
import httpx
from bs4 import BeautifulSoup


def fetch_web_content(url: str) -> dict:
    """Fetch and extract readable text from a webpage."""

    headers = {
        "User-Agent": "Mozilla/5.0 CryptoPulseAI/1.0"
    }

    response = httpx.get(
        url,
        headers=headers,
        timeout=30.0,
        follow_redirects=True,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove elements that don't contain useful article content.
    for element in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "noscript",
    ]):
        element.decompose()

    # Prefer the main article content when available.
    content = (
        soup.find("article")
        or soup.find("main")
        or soup.body
        or soup
    )

    title = soup.title.get_text(strip=True) if soup.title else ""

    text = content.get_text(separator="\n", strip=True)

    return {
        "url": str(response.url),
        "title": title,
        "content": text[:20000],
        "word_count": len(text.split()),
    }
