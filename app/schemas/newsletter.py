
from datetime import date, datetime, timezone

from pydantic import BaseModel, Field

from app.schemas.article import Article


class NewsletterSection(BaseModel):
    title: str = Field(min_length=2)

    description: str | None = None

    articles: list[Article] = Field(default_factory=list)


class Newsletter(BaseModel):
    issue_id: str

    title: str = "CryptoPulse AI - FinTech Intelligence Briefing"

    issue_date: date = Field(default_factory=date.today)

    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    introduction: str | None = None

    sections: list[NewsletterSection] = Field(default_factory=list)

    key_takeaways: list[str] = Field(default_factory=list)

    total_articles: int = 0

    status: str = "draft"
