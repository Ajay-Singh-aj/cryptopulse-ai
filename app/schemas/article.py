
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, HttpUrl, ConfigDict


class ArticleCategory(str, Enum):
    CRYPTOGRAPHY = "cryptography"
    PAYMENT_SECURITY = "payment_security"
    FINTECH_REGULATION = "fintech_regulation"
    CYBERSECURITY = "cybersecurity"


class SourceType(str, Enum):
    WEB = "web"
    RESEARCH_PAPER = "research_paper"
    OFFICIAL_ANNOUNCEMENT = "official_announcement"
    SECURITY_ADVISORY = "security_advisory"


class Article(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        str_strip_whitespace=True,
    )

    title: str = Field(min_length=5, max_length=500)

    url: HttpUrl

    source_name: str = Field(min_length=2)

    source_type: SourceType

    category: ArticleCategory

    description: str | None = None

    authors: list[str] = Field(default_factory=list)

    published_at: datetime | None = None

    discovered_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    relevance_score: int = Field(
        default=0,
        ge=0,
        le=100,
    )

    summary: str | None = None

    fintech_impact: str | None = None

    keywords: list[str] = Field(default_factory=list)

    verified: bool = False

    metadata: dict[str, Any] = Field(default_factory=dict)
