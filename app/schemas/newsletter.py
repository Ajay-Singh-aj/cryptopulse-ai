from datetime import date, datetime, timezone

from pydantic import BaseModel, Field, HttpUrl

from app.schemas.article import Article


class NewsletterSection(BaseModel):
    title: str = Field(min_length=2)

    description: str | None = None

    articles: list[Article] = Field(default_factory=list)


class NewsletterReference(BaseModel):
    label: str = Field(min_length=2)
    url: HttpUrl


class Newsletter(BaseModel):
    issue_id: str

    title: str = "CryptoPulse AI - FinTech Intelligence Briefing"

    issue_date: date = Field(default_factory=date.today)

    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    introduction: str | None = None

    freshness_note: str | None = None

    real_world_problem: str | None = None

    fintech_impact: str | None = None

    india_relevance: list[str] = Field(default_factory=list)

    authentication_factors: list[str] = Field(default_factory=list)

    sections: list[NewsletterSection] = Field(default_factory=list)

    key_takeaways: list[str] = Field(default_factory=list)

    key_findings: list[str] = Field(default_factory=list)

    why_read: str | None = None

    technical_flow_title: str | None = None

    technical_flow_steps: list[str] = Field(default_factory=list)

    context_sources: list[NewsletterReference] = Field(default_factory=list)

    total_articles: int = 0

    status: str = "draft"
