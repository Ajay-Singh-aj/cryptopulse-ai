
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    APP_NAME: str = "CryptoPulse AI"
    APP_ENV: Literal["development", "production"] = "development"
    TIMEZONE: str = "Asia/Kolkata"

    # LLM Configuration
    LLM_PROVIDER: Literal["groq", "huggingface"] = "groq"
    LLM_MODEL: str = ""
    LLM_TEMPERATURE: float = Field(default=0.2, ge=0, le=1)
    LLM_MAX_TOKENS: int = Field(default=2048, gt=0)

    GROQ_API_KEY: SecretStr | None = None
    HUGGINGFACE_API_KEY: SecretStr | None = None

    # Research Configuration
    TAVILY_API_KEY: SecretStr | None = None
    TAVILY_MAX_RESULTS: int = Field(default=5, ge=1, le=20)
    TAVILY_SEARCH_DEPTH: Literal["basic", "advanced"] = "basic"
    MAX_RESEARCH_ITERATIONS: int = Field(default=2, ge=1, le=5)

    # Database
    DATABASE_URL: str = "sqlite:///./data/cryptopulse.db"
    DRY_RUN: bool = True

    # Email
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_SENDER: str = ""
    EMAIL_PASSWORD: SecretStr | None = None

    # Newsletter
    NEWSLETTER_HOUR: int = Field(default=11, ge=0, le=23)
    NEWSLETTER_MINUTE: int = Field(default=0, ge=0, le=59)
    NEWSLETTER_DAYS: list[int] = [0, 2, 4]

    MAX_ARTICLES_PER_NEWSLETTER: int = Field(default=1, ge=1, le=30)
    MIN_RELEVANCE_SCORE: int = Field(default=60, ge=0, le=100)


@lru_cache
def get_settings() -> Settings:
    return Settings()
