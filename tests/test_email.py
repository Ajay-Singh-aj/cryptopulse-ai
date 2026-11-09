
from unittest.mock import patch, MagicMock

from app.services.email_service import send_email


@patch("app.services.email_service.smtplib.SMTP")
def test_send_email(mock_smtp):
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    send_email(
        subject="CryptoPulse AI Test",
        html_content="<h1>Hello CryptoPulse</h1>",
        recipients=["test@example.com"],
        text_content="Hello CryptoPulse",
    )

    mock_smtp.assert_called_once()
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()
