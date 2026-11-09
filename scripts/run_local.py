
from app.config.logging_config import setup_logging, get_logger
from app.database import get_connection, create_tables
from app.graph.workflow import crypto_pulse_workflow
from app.services.delivery_service import deliver_newsletter


def main():
    setup_logging()
    logger = get_logger(__name__)

    logger.info("Starting CryptoPulse AI...")

    try:
        # Initialize database tables.
        with get_connection() as connection:
            create_tables(connection)

        logger.info("Database initialized.")

        # Generate newsletter.
        result = crypto_pulse_workflow.invoke({})
        newsletter = result.get("newsletter")

        if not newsletter:
            logger.warning("No newsletter was generated.")
            return

        logger.info("Newsletter generated.")
        logger.info("Issue ID: %s", newsletter.issue_id)
        logger.info("Articles: %s", newsletter.total_articles)

        # Deliver newsletter.
        delivery_result = deliver_newsletter(newsletter)

        logger.info("Delivery completed.")
        logger.info("Total subscribers: %s", delivery_result["total"])
        logger.info("Successfully sent: %s", delivery_result["sent"])
        logger.info("Failed: %s", delivery_result["failed"])

    except Exception:
        logger.exception("CryptoPulse AI workflow failed.")
        raise


if __name__ == "__main__":
    main()
