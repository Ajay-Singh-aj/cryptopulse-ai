
from app.config.logging_config import setup_logging, get_logger
from app.graph.workflow import crypto_pulse_workflow


def main():
    """Run the CryptoPulse AI newsletter workflow."""

    setup_logging()
    logger = get_logger(__name__)

    logger.info("Starting CryptoPulse AI...")

    try:
        result = crypto_pulse_workflow.invoke({})

        newsletter = result.get("newsletter")

        if newsletter:
            logger.info("Newsletter generated successfully.")
            logger.info("Issue ID: %s", newsletter.issue_id)
            logger.info("Total articles: %s", newsletter.total_articles)
            logger.info("Status: %s", newsletter.status)
        else:
            logger.warning("No newsletter was generated.")

        errors = result.get("research_errors", [])

        for error in errors:
            logger.error("Research error: %s", error)

    except Exception:
        logger.exception("CryptoPulse AI workflow failed.")
        raise


if __name__ == "__main__":
    main()
