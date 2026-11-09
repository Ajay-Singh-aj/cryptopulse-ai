from app.graph.workflow import crypto_pulse_workflow
from app.database import get_active_subscribers
from app.database.repository import save_newsletter, record_delivery
from app.services.render_service import render_newsletter_html
from app.services.email_service import send_email


def main():
    print("Starting one-time newsletter delivery...")

    # Require exactly one active subscriber.
    subscribers = get_active_subscribers()

    if len(subscribers) != 1:
        raise RuntimeError(
            f"Expected exactly 1 active subscriber, found {len(subscribers)}."
        )

    subscriber = subscribers[0]

    confirmation = input(
        f"Send newsletter to {subscriber['email']}? Type YES to confirm: "
    )

    if confirmation != "YES":
        print("Delivery cancelled.")
        return

    # Generate newsletter.
    result = crypto_pulse_workflow.invoke({})
    newsletter = result.get("newsletter")

    if not newsletter or newsletter.total_articles == 0:
        raise RuntimeError("No newsletter with articles was generated.")

    # Render and save.
    html_content = render_newsletter_html(newsletter)
    newsletter_id = save_newsletter(
        newsletter,
        html_content=html_content,
    )

    # Send only to the confirmed subscriber.
    send_email(
        subject=newsletter.title,
        html_content=html_content,
        recipients=[subscriber["email"]],
        text_content=newsletter.introduction or newsletter.title,
    )

    record_delivery(
        newsletter_id=newsletter_id,
        subscriber_id=subscriber["id"],
        status="sent",
    )

    print("Newsletter sent successfully!")
    print(f"Recipient: {subscriber['email']}")
    print(f"Articles: {newsletter.total_articles}")


if __name__ == "__main__":
    main()
