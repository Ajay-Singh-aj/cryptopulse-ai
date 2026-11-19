from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from pydantic import SecretStr

from app.services.email_service import send_email


@patch("app.services.email_service.smtplib.SMTP")
@patch("app.services.email_service.get_settings")
def test_send_email(mock_get_settings, mock_smtp):
    """Verify SMTP setup without requiring secrets or sending a real email."""

    mock_get_settings.return_value = SimpleNamespace(
        EMAIL_SENDER="sender@example.com",
        EMAIL_PASSWORD=SecretStr("test-password"),
        EMAIL_HOST="smtp.example.com",
        EMAIL_PORT=587,
    )

    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    send_email(
        subject="CryptoPulse AI Test",
        html_content="<h1>Hello CryptoPulse</h1>",
        recipients=["test@example.com"],
        text_content="Hello CryptoPulse",
    )

    mock_smtp.assert_called_once_with("smtp.example.com", 587)
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with(
        "sender@example.com",
        "test-password",
    )
    mock_server.send_message.assert_called_once()
