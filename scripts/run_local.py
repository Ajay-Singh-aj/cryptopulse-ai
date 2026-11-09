
from app.config import get_settings
from app.config.logging_config import setup_logging, get_logger
from app.database import get_connection, create_tables
from app.graph.workflow import crypto_pulse_workflow
from app.services.newsletter_service import create_newsletter
from app.services.render_service import render_newsletter_html
from app.database import save_newsletter
from app.services.delivery_service import deliver_newsletter


def main():
    setup_logging()
    logger = get_logger(__name__)
    settings = get_settings()

    logger.info("Starting CryptoPulse AI...")
    logger.info("Dry run mode: %s", settings.DRY_RUN)

    try:
        # Initialize database.
        with get_connection() as connection:
            create_tables(connection)

        logger.info("Database initialized.")

        # Generate newsletter.
        result = crypto_pulse_workflow.invoke({})
        newsletter = result.get("newsletter")

        if not newsletter:
            logger.warning("No newsletter was generated.")
            return

        if newsletter.total_articles == 0:
            logger.warning("Newsletter contains no articles. Delivery skipped.")
            return

        logger.info("Newsletter generated.")
        logger.info("Issue ID: %s", newsletter.issue_id)
        logger.info("Articles: %s", newsletter.total_articles)

        # Save only during dry run; never send emails.
        if settings.DRY_RUN:
            html_content = render_newsletter_html(newsletter)
            save_newsletter(newsletter, html_content=html_content)
            logger.info("Dry run completed. Newsletter saved; no emails sent.")
            return

        # Live delivery.
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
