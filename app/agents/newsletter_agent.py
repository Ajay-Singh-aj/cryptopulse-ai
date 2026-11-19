from app.schemas.article import Article
from app.schemas.newsletter import Newsletter, NewsletterReference
from app.services.llm_service import get_llm
from app.services.newsletter_service import create_newsletter
from app.utils.date_utils import get_current_date


RBI_AUTHENTICATION_REFERENCE = (
    "RBI Authentication Mechanisms for Digital Payment Transactions "
    "Directions, 2025",
    "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12898",
)
NPCI_UPI_AUTHENTICATION_REFERENCE = (
    "NPCI UPI Operating Circular 226: Additional Authentication Methods",
    "https://www.npci.org.in/uploads/UPI_OC_226_Introduction_of_Additional_"
    "Authentication_methods_in_UPI_ec075a3a14.pdf",
)

AUTHENTICATION_TERMS = (
    "authentication", "multi-factor", "multifactor", "two-factor",
    "2fa", "mfa", "otp", "biometric", "upi pin", "passkey",
    "identity verification", "device binding",
)
INDIA_PAYMENT_TERMS = (
    "rbi", "npci", "upi", "rupay", "aeps", "imps", "nach",
    "netc", "fastag", "bharat billpay", "indian payment",
    "india payment", "digital payment in india",
)


def _parse_bullets(text: str) -> list[str]:
    """Extract concise bullet items from a model-generated section."""
    items = []
    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned.startswith(("-", "•", "*")):
            cleaned = cleaned.lstrip("-•* ").strip()
        elif cleaned[:2].rstrip(".").isdigit():
            cleaned = cleaned[2:].lstrip(".) ").strip()
        else:
            continue
        if cleaned:
            items.append(cleaned)
    return items


def _section_text(output: str, labels: list[str]) -> dict[str, str]:
    """Split model output by exact section headings, tolerating Markdown."""
    buffers = {label: [] for label in labels}
    current = None

    for line in output.splitlines():
        stripped = line.strip()
        normalized = stripped.strip("#*_ \\t`").upper()
        matched = next(
            (label for label in labels if normalized == label),
            None,
        )
        if matched:
            current = matched
        elif current:
            buffers[current].append(line)

    return {
        label: "\\n".join(lines).strip()
        for label, lines in buffers.items()
    }


def _topic_flags(articles: list[Article]) -> tuple[bool, bool]:
    text = " ".join(
        " ".join([
            article.title,
            article.description or "",
            article.summary or "",
            " ".join(article.keywords),
            article.source_name,
        ])
        for article in articles
    ).lower()

    authentication_related = any(term in text for term in AUTHENTICATION_TERMS)
    india_payment_related = any(term in text for term in INDIA_PAYMENT_TERMS)
    return authentication_related, india_payment_related


def _build_context_sources(
    articles: list[Article],
    authentication_related: bool,
    india_payment_related: bool,
) -> list[NewsletterReference]:
    """Keep traceable links for every piece of official context shown."""
    references = []
    seen_urls = set()

    for article in articles:
        raw_context = article.metadata.get("current_context", [])
        if not isinstance(raw_context, list):
            continue

        for item in raw_context:
            if not isinstance(item, dict):
                continue
            url = item.get("url")
            label = item.get("title") or "Official context"
            if not url or url in seen_urls:
                continue
            try:
                references.append(
                    NewsletterReference(label=str(label)[:160], url=url)
                )
                seen_urls.add(url)
            except Exception:
                continue

    if authentication_related and india_payment_related:
        for label, url in (
            RBI_AUTHENTICATION_REFERENCE,
            NPCI_UPI_AUTHENTICATION_REFERENCE,
        ):
            if url not in seen_urls:
                references.append(NewsletterReference(label=label, url=url))
                seen_urls.add(url)

    return references[:5]


def generate_newsletter(articles: list[Article]) -> Newsletter:
    """Generate a topic-aware, source-grounded editorial briefing."""

    newsletter = create_newsletter(articles)

    if not articles:
        return newsletter

    # Generate all editorial analysis from the same lead article that will be sent.
    selected_articles = [
        article
        for section in newsletter.sections
        for article in section.articles
    ]
    if not selected_articles:
        return newsletter

    llm = get_llm()
    current_date = get_current_date().isoformat()
    authentication_related, india_payment_related = _topic_flags(selected_articles)

    article_context = "\\n\\n".join(
        f"Title: {article.title}\\n"
        f"Source: {article.source_name}\\n"
        f"Published: {article.published_at or 'Date not supplied'}\\n"
        f"URL: {article.url}\\n"
        f"Summary: {article.summary or article.description or 'Not available'}\\n"
        f"Fintech impact: {article.fintech_impact or 'Not specified'}\\n"
        f"Official current context: "
        f"{article.metadata.get('current_context', [])}"
        for article in selected_articles
    )

    authentication_context = ""
    if authentication_related and india_payment_related:
        authentication_context = """
VERIFIED INDIA DIGITAL-PAYMENT AUTHENTICATION CONTEXT
Use this only if it directly applies to the article; keep its scope and date clear.

RBI Directions (25 September 2025; compliance date 1 April 2026):
- Domestic digital payment transactions require at least two distinct
  authentication factors, unless an applicable exemption applies.
- For transactions other than card-present transactions, at least one factor
  must be dynamically created or proven and unique to that transaction.
- RBI describes three possible factor classes:
  (1) something the user knows, (2) something the user has,
  (3) something the user is.
- The three classes are not a requirement to use all three. The rule is at
  least two distinct factors, subject to the applicable exemptions.

NPCI UPI Operating Circular 226 (7 October 2025):
- The circular says UPI PIN is used for transaction authentication in current
  UPI functionality, except UPI Lite and mandate execution.
- It introduces optional additional methods: UIDAI face authentication as an
  option for setting/resetting a UPI PIN in place of card credentials or
  Aadhaar OTP; and on-device biometrics as an option in place of UPI PIN for
  UPI transactions, initially up to Rs 5,000.
- Issuer banks, PSP banks and UPI apps may implement these options. Do not
  imply every bank/app has deployed them or that biometrics are mandatory.
- Describe biometric transaction authentication as an alternative to the PIN
  where the circular says "in lieu of", not as an extra third factor.
- Do not assume that all NPCI products use UPI's authentication design.
- Do not call device possession a factor in a particular flow unless the
  source establishes how that device is bound and validated.
"""

    prompt = f"""
You are the senior editorial analyst of CryptoPulse AI, a specialist
cryptography, cybersecurity and fintech intelligence briefing.

CURRENT DATE: {current_date}

SOURCE MATERIAL
{article_context}

{authentication_context}

Create a concise but substantive, topic-aware briefing. The article may be
old; do not present an old circular or announcement as breaking news.

Return these exact section headings, in this order. Leave a section empty
when it genuinely does not apply; do not force irrelevant content.

INTRODUCTION:
2 concise sentences stating the development and why it matters.

FRESHNESS / CURRENT STATUS:
State the original publication/issue date and effective date separately when
available. Explain whether this is new, historical background, already in
force, phased, optional, or still awaiting implementation only when supported.
Use the recent official context supplied above. If no current official status
was found, say that rollout/current implementation is not confirmed by the
available sources. Do not confuse a circular's date with its effective date.

REAL-WORLD PROBLEM:
Describe one concrete real-world problem, who experiences it (customer, bank,
merchant, payment operator, developer, security team), how it happens, and
what the development changes. Use a practical scenario, not generic claims.

INDIA / NPCI PRODUCT RELEVANCE:
Only for an India/payment-related topic. Identify the exact NPCI product or
payment workflow directly affected (for example UPI, UPI Lite, IMPS, RuPay,
AePS, NACH, BBPS/Bharat Connect, or NETC/FASTag) and explain the actual
touchpoint and reason. Distinguish direct impact from indirect context.
Name only products supported by the source material or official context.
If no direct product mapping is supported, say so. Never imply one RBI/NPCI
rule applies identically to every NPCI product.

KEY SUMMARY:
2-3 short, high-value bullets explaining the central development.

KEY FINDINGS:
3-5 factual bullets with important mechanisms, limits, dates, actors, figures,
exceptions or implementation responsibilities. Avoid repeating the summary.

AUTHENTICATION FACTORS:
Only when authentication is relevant. Explain these three classes in plain
language, using labelled bullets:
- WHAT YOU KNOW: a PIN, password or passphrase.
- WHAT YOU HAVE: a card, hardware/software token, or OTP delivered to a
  controlled device/channel, when the scheme treats it as a possession factor.
- WHAT YOU ARE: a biometric such as fingerprint or face.
Then identify which factor(s) the actual product uses, what is optional or
alternative, and whether two distinct factors are required. Do not say all
three are always required. Do not conflate two examples from the same class
with two independent factors.

FINTECH IMPACT:
Explain the concrete operational, customer, security or compliance implication.
Name the affected product only when supported.

TECHNICAL FLOW TITLE:
A short title for a useful flow diagram, or leave empty.

TECHNICAL FLOW STEPS:
If the source describes a process that benefits from a diagram, provide 3-5
ordered bullets in the form "Actor: action — result". Examples include a
payment/authentication journey, key exchange, certificate validation,
incident response or settlement flow. Only include supported steps. If no
clear sequence exists, leave empty rather than inventing a diagram.

WHY YOU SHOULD READ THIS:
2-3 specific sentences explaining who should read it and what decision,
risk, implementation detail or practical understanding they gain.

EDITORIAL RULES:
- Separate source facts, official current context, and analytical interpretation.
- Use the freshest official context supplied, but never assume it is exhaustive.
- If a source is older than 90 days, label it as background/historical and
  explain what remains relevant today only when verified.
- State when a product mapping, current rollout, or effect is not established.
- Do not invent use cases, product dependencies, transaction limits, factors,
  numbers, dates, legal obligations or deployment status.
- Prefer simple explanations without losing technical accuracy.
- Do not repeat the same information across sections.
- Return only the labelled sections; no extra preamble or Markdown fences.
"""

    try:
        response = llm.invoke(prompt)
        output = response.content or ""

        labels = [
            "INTRODUCTION:",
            "FRESHNESS / CURRENT STATUS:",
            "REAL-WORLD PROBLEM:",
            "INDIA / NPCI PRODUCT RELEVANCE:",
            "FINTECH IMPACT:",
            "KEY SUMMARY:",
            "KEY FINDINGS:",
            "AUTHENTICATION FACTORS:",
            "TECHNICAL FLOW TITLE:",
            "TECHNICAL FLOW STEPS:",
            "WHY YOU SHOULD READ THIS:",
        ]
        sections = _section_text(output, labels)

        introduction = sections["INTRODUCTION:"] or newsletter.introduction or ""
        key_summary = _parse_bullets(sections["KEY SUMMARY:"])
        key_findings = _parse_bullets(sections["KEY FINDINGS:"])
        auth_factors = _parse_bullets(sections["AUTHENTICATION FACTORS:"])
        india_relevance = _parse_bullets(
            sections["INDIA / NPCI PRODUCT RELEVANCE:"]
        )
        flow_steps = _parse_bullets(sections["TECHNICAL FLOW STEPS:"])[:5]
        flow_title = sections["TECHNICAL FLOW TITLE:"].splitlines()[0].strip() if (
            sections["TECHNICAL FLOW TITLE:"]
        ) else None

        # Retain useful content if a model response omits a section.
        if not key_summary:
            key_summary = [
                article.summary or article.description
                for article in articles
                if article.summary or article.description
            ][:3]
        if not key_findings:
            key_findings = [
                article.fintech_impact
                for article in articles
                if article.fintech_impact
            ][:3]

        why_read = sections["WHY YOU SHOULD READ THIS:"] or (
            "Read the original source for the complete detail, scope and "
            "implementation requirements behind this development."
        )

        references = _build_context_sources(
            selected_articles,
            authentication_related,
            india_payment_related,
        )

        return newsletter.model_copy(
            update={
                "introduction": introduction,
                "freshness_note": sections["FRESHNESS / CURRENT STATUS:"] or None,
                "real_world_problem": sections["REAL-WORLD PROBLEM:"] or None,
                "fintech_impact": sections["FINTECH IMPACT:"] or None,
                "india_relevance": india_relevance,
                "authentication_factors": auth_factors,
                "key_takeaways": key_summary,
                "key_findings": key_findings,
                "why_read": why_read,
                "technical_flow_title": flow_title if len(flow_steps) >= 3 else None,
                "technical_flow_steps": flow_steps if len(flow_steps) >= 3 else [],
                "context_sources": references,
            }
        )

    except Exception:
        return newsletter
