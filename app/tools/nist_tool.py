
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

NIST_PQC_URL = (
    "https://csrc.nist.gov/Projects/post-quantum-cryptography/news"
)


def search_nist(max_results: int = 10) -> list[dict]:
    """Retrieve NIST PQC news articles."""

    response = httpx.get(
        NIST_PQC_URL,
        timeout=30.0,
        follow_redirects=True,
        headers={"User-Agent": "Mozilla/5.0 CryptoPulseAI/1.0"},
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    seen_urls = set()

    # Extract links from the main page content only
    main_content = soup.find("main") or soup

    for link in main_content.find_all("a", href=True):
        title = link.get_text(" ", strip=True)
        url = urljoin(NIST_PQC_URL, link["href"])

        if not title or len(title) < 20:
            continue

        if "/Projects/post-quantum-cryptography/" not in url:
            continue

        if url.rstrip("/") == NIST_PQC_URL.rstrip("/"):
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)

        articles.append({
            "title": title,
            "url": url,
            "source_name": "NIST",
            "source_type": "official_announcement",
        })

        if len(articles) >= max_results:
            break

    return articles
