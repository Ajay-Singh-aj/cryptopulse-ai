
import httpx
from bs4 import BeautifulSoup

MIRROR_URL = "https://eprint.iacr.asia/days/7"


def search_iacr(max_results: int = 10) -> list[dict]:
    """Retrieve recent cryptography papers from the IACR mirror."""

    response = httpx.get(
        MIRROR_URL,
        timeout=30.0,
        follow_redirects=True,
        headers={"User-Agent": "CryptoPulseAI/1.0"},
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    papers = []

    for heading in soup.find_all(["h2", "h3", "h4"]):
        title = heading.get_text(" ", strip=True)

        link = heading.find("a", href=True)

        if not link:
            link = heading.find_next("a", href=True)

        if not link:
            continue

        href = link["href"]

        if href.startswith("/"):
            href = MIRROR_URL.rstrip("/") + href

        papers.append({
            "title": title,
            "url": href,
            "source_name": "IACR Cryptology ePrint",
            "source_type": "research_paper",
        })

        if len(papers) >= max_results:
            break

    return papers
