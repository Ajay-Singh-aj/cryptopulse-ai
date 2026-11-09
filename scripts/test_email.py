
from app.config.logging_config import setup_logging
from app.services.email_service import send_email


def main():
    setup_logging()

    recipient = input("Enter recipient email address: ").strip()

    if not recipient:
        print("Recipient email is required.")
        return

    try:
        send_email(
            subject="CryptoPulse AI - Email Test",
            html_content="""
                <html>
                    <body>
                        <h2>CryptoPulse AI</h2>
                        <p>Your email service is working successfully!</p>
                        <p>Your fintech intelligence newsletter is getting ready.</p>
                    </body>
                </html>
            """,
            recipients=[recipient],
            text_content="CryptoPulse AI email service is working!",
        )

        print(f"Test email sent to {recipient}")

    except Exception as exc:
        print(f"Email sending failed: {exc}")


if __name__ == "__main__":
    main()
