
import logging

from app.config.logging_config import get_logger, setup_logging


def get_module_logger(module_name: str) -> logging.Logger:
    """Return a logger for the requested module."""
    return get_logger(module_name)


def log_exception(
    logger: logging.Logger,
    message: str,
) -> None:
    """Log an error with its exception traceback."""
    logger.exception(message)


def initialize_logger() -> None:
    """Initialize application-wide logging."""
    setup_logging()
