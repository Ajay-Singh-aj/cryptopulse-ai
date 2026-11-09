
from unittest.mock import Mock

from app.schemas.newsletter import Newsletter
from app.services import delivery_service


def test_deliver_newsletter(monkeypatch):
    """Test newsletter delivery without sending real emails."""

    newsletter = Newsletter(
        issue_id="test-issue-001",
        title="CryptoPulse AI - Test Newsletter",
        introduction="Test newsletter introduction.",
    )

    subscribers = [
        {
            "id": 1,
            "email": "alice@example.com",
        },
        {
            "id": 2,
            "email": "bob@example.com",
        },
    ]

    # Mock database operations.
    monkeypatch.setattr(
        delivery_service,
        "get_active_subscribers",
        lambda: subscribers,
    )

    save_mock = Mock(return_value=10)
    monkeypatch.setattr(
        delivery_service,
        "save_newsletter",
        save_mock,
    )

    record_mock = Mock()
    monkeypatch.setattr(
        delivery_service,
        "record_delivery",
        record_mock,
    )

    # Mock HTML rendering.
    monkeypatch.setattr(
        delivery_service,
        "render_newsletter_html",
        lambda newsletter: "<h1>Test Newsletter</h1>",
    )

    # Mock email sending.
    email_mock = Mock()
    monkeypatch.setattr(
        delivery_service,
        "send_email",
        email_mock,
    )

    # Execute delivery.
    result = delivery_service.deliver_newsletter(newsletter)

    # Verify results.
    assert result["total"] == 2
    assert result["sent"] == 2
    assert result["failed"] == 0

    assert email_mock.call_count == 2
    assert record_mock.call_count == 2
    assert save_mock.call_count == 1

    # Verify recipients are emailed individually.
    recipients = [
        call.kwargs["recipients"]
        for call in email_mock.call_args_list
    ]

    assert recipients == [
        ["alice@example.com"],
        ["bob@example.com"],
    ]

def test_delivery_continues_after_email_failure(monkeypatch):
    """Ensure one failed email doesn't stop other deliveries."""

    newsletter = Newsletter(
        issue_id="test-issue-002",
        title="CryptoPulse AI - Failure Test",
    )

    subscribers = [
        {"id": 1, "email": "alice@example.com"},
        {"id": 2, "email": "bob@example.com"},
    ]

    monkeypatch.setattr(
        delivery_service,
        "get_active_subscribers",
        lambda: subscribers,
    )

    monkeypatch.setattr(
        delivery_service,
        "save_newsletter",
        lambda *args, **kwargs: 20,
    )

    monkeypatch.setattr(
        delivery_service,
        "render_newsletter_html",
        lambda newsletter: "<h1>Test</h1>",
    )

    def mock_send_email(**kwargs):
        if kwargs["recipients"] == ["alice@example.com"]:
            raise RuntimeError("Simulated email failure")

    monkeypatch.setattr(
        delivery_service,
        "send_email",
        mock_send_email,
    )

    recorded_deliveries = []

    monkeypatch.setattr(
        delivery_service,
        "record_delivery",
        lambda **kwargs: recorded_deliveries.append(kwargs),
    )

    result = delivery_service.deliver_newsletter(newsletter)

    assert result["total"] == 2
    assert result["sent"] == 1
    assert result["failed"] == 1

    assert recorded_deliveries[0]["status"] == "failed"
    assert recorded_deliveries[1]["status"] == "sent"
