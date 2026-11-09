
from datetime import datetime, timezone

from pydantic import BaseModel, Field

from app.schemas.article import Article


class ResearchQuery(BaseModel):
    query: str = Field(min_length=3)
    topic: str
    source: str | None = None
    max_results: int = Field(default=5, ge=1, le=20)


class ResearchBatch(BaseModel):
    execution_id: str

    queries: list[ResearchQuery] = Field(default_factory=list)

    articles: list[Article] = Field(default_factory=list)

    total_results: int = 0

    started_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    completed_at: datetime | None = None

    errors: list[str] = Field(default_factory=list)

    @property
    def successful(self) -> bool:
        return len(self.articles) > 0
