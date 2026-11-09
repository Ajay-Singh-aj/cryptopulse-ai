from app.database import add_subscriber
from app.schemas.subscriber import Subscriber


def main():
    email = input("Enter subscriber email: ").strip().lower()

    if not email:
        print("Email cannot be empty.")
        return

    subscriber = Subscriber(
        email=email,
        is_active=True,
        preferred_topics=[],
        receive_research_papers=True,
        receive_industry_news=True,
    )

    subscriber_id = add_subscriber(subscriber)

    print(f"Subscriber registered successfully!")
    print(f"Subscriber ID: {subscriber_id}")


if __name__ == "__main__":
    main()