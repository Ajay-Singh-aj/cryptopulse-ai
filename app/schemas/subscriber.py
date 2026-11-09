
from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr, Field


class Subscriber(BaseModel):

    email: EmailStr

    name: str | None = None

    is_active: bool = True

    preferred_topics: list[str] = Field(
        default_factory=list
    )

    receive_research_papers: bool = True

    receive_industry_news: bool = True

    subscribed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
