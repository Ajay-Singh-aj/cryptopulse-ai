
from app.graph.workflow import crypto_pulse_workflow


def main():
    print("Starting CryptoPulse AI generation test...")

    result = crypto_pulse_workflow.invoke({})

    raw_articles = result.get("articles", [])
    relevant_articles = result.get("relevant_articles", [])
    verified_articles = result.get("verified_articles", [])
    analyzed_articles = result.get("analyzed_articles", [])
    newsletter = result.get("newsletter")

    print("\n========== GENERATION REPORT ==========")
    print(f"Articles collected: {len(raw_articles)}")
    print(f"Relevant articles: {len(relevant_articles)}")
    print(f"Verified articles: {len(verified_articles)}")
    print(f"Analyzed articles: {len(analyzed_articles)}")

    if newsletter:
        print(f"Newsletter title: {newsletter.title}")
        print(f"Newsletter articles: {newsletter.total_articles}")
        print(f"Introduction generated: {bool(newsletter.introduction)}")
    else:
        print("Newsletter was not generated.")

    print("=======================================")


if __name__ == "__main__":
    main()
