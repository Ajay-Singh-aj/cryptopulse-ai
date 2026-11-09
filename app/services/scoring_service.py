
from app.schemas.article import Article


KEYWORDS = {
    "cryptography": [
        "cryptography",
        "post-quantum",
        "quantum-resistant",
        "zero-knowledge",
        "homomorphic encryption",
        "multi-party computation",
        "digital signature",
        "elliptic curve",
    ],
    "payment_security": [
        "upi",
        "payment security",
        "payment tokenization",
        "transaction security",
        "authentication",
        "payment fraud",
    ],
    "fintech_regulation": [
        "npci",
        "rbi",
        "digital payments",
        "payment system",
        "financial regulation",
    ],
    "cybersecurity": [
        "cybersecurity",
        "vulnerability",
        "security advisory",
        "encryption attack",
        "data breach",
        "key management",
    ],
}


def score_article(article: Article) -> int:
    """Calculate an article's relevance score from 0 to 100."""

    text = " ".join([
        article.title or "",
        article.description or "",
        " ".join(article.keywords),
    ]).lower()

    category = str(article.category)
    category_keywords = KEYWORDS.get(category, [])

    score = 30  # Base score for a candidate article.

    # Reward matches in the article's category.
    for keyword in category_keywords:
        if keyword in text:
            score += 10

    # Give additional weight to highly relevant technical terms.
    high_priority_terms = [
        "post-quantum",
        "zero-knowledge",
        "homomorphic encryption",
        "upi security",
        "payment security",
        "cyber resilience",
    ]

    for keyword in high_priority_terms:
        if keyword in text:
            score += 10

    return min(score, 100)


def score_articles(articles: list[Article]) -> list[Article]:
    """Return articles with updated relevance scores."""

    scored_articles = []

    for article in articles:
        score = score_article(article)

        scored_articles.append(
            article.model_copy(update={"relevance_score": score})
        )

    return sorted(
        scored_articles,
        key=lambda article: article.relevance_score,
        reverse=True,
    )
