
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

CERTIN_URL = (
    "https://www.cert-in.org.in/"
    "s2cMainServlet?pageid=PUBADVLIST02"
)


def search_certin(max_results: int = 10) -> list[dict]:
    """Retrieve CERT-In cybersecurity advisories."""

    response = httpx.get(
        CERTIN_URL,
        timeout=30.0,
        follow_redirects=True,
        headers={"User-Agent": "Mozilla/5.0 CryptoPulseAI/1.0"},
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    advisories = []
    seen_urls = set()

    for link in soup.find_all("a", href=True):
        title = link.get_text(" ", strip=True)
        url = urljoin(CERTIN_URL, link["href"])

        if not title or url in seen_urls:
            continue

        if "VLCODE=CIAD-" not in url:
            continue

        seen_urls.add(url)
        advisories.append({
            "title": title,
            "url": url,
            "source_name": "CERT-In",
            "source_type": "security_advisory",
        })

        if len(advisories) >= max_results:
            break

    return advisories
