
import smtplib
from email.message import EmailMessage

from app.config import get_settings


def send_email(
    subject: str,
    html_content: str,
    recipients: list[str],
    text_content: str | None = None,
) -> None:
    """Send an HTML email to one or more recipients."""

    settings = get_settings()

    if not settings.EMAIL_SENDER:
        raise ValueError("EMAIL_SENDER is missing from .env")

    if not settings.EMAIL_PASSWORD:
        raise ValueError("EMAIL_PASSWORD is missing from .env")

    if not recipients:
        raise ValueError("At least one recipient is required")

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.EMAIL_SENDER
    message["To"] = ", ".join(recipients)

    message.set_content(
        text_content or "Please view this newsletter in an HTML-compatible email client."
    )
    message.add_alternative(html_content, subtype="html")

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(
            settings.EMAIL_SENDER,
            settings.EMAIL_PASSWORD.get_secret_value(),
        )
        server.send_message(message)
