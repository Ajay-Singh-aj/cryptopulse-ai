
from functools import lru_cache

from langchain_groq import ChatGroq

from app.config import get_settings


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    """Initialize and return the configured Groq LLM."""

    settings = get_settings()

    if settings.LLM_PROVIDER != "groq":
        raise ValueError(
            f"Unsupported LLM provider: {settings.LLM_PROVIDER}"
        )

    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing from .env")

    if not settings.LLM_MODEL:
        raise ValueError("LLM_MODEL is missing from .env")

    return ChatGroq(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        max_tokens=settings.LLM_MAX_TOKENS,
        api_key=settings.GROQ_API_KEY.get_secret_value(),
        max_retries=5,
        timeout=60,
    )
