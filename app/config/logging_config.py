
import logging
from pathlib import Path

from app.config.settings import get_settings


def setup_logging() -> None:
    settings = get_settings()

    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_level = (
        logging.DEBUG
        if settings.APP_ENV == "development"
        else logging.INFO
    )

    logging.basicConfig(
        level=log_level,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                log_dir / "cryptopulse.log",
                encoding="utf-8",
            ),
        ],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
