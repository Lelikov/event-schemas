"""Tests for the canonical {"original", "normalized"} envelope."""

from event_schemas.envelope import EventEnvelope, unwrap_payload
from event_schemas.notification import NotificationCommandPayload


def test_unwrap_payload_returns_original_section() -> None:
    data = {"original": {"booking_id": "b-1"}, "normalized": {"participants": []}}

    assert unwrap_payload(data) == {"booking_id": "b-1"}


def test_unwrap_payload_tolerates_bare_payload() -> None:
    data = {"booking_id": "b-1"}

    assert unwrap_payload(data) == {"booking_id": "b-1"}


def test_unwrap_payload_handles_none_and_empty() -> None:
    assert unwrap_payload(None) == {}
    assert unwrap_payload({}) == {}


def test_envelope_exposes_normalized_participants_with_user_id() -> None:
    envelope = EventEnvelope.model_validate(
        {
            "original": {"booking_id": "b-1"},
            "normalized": {
                "participants": [
                    {"email": "org@example.com", "role": "organizer", "user_id": "uuid-1"},
                    {"email": "cli@example.com", "role": "client"},
                ]
            },
        }
    )

    participants = envelope.normalized.participants
    assert participants[0].user_id == "uuid-1"
    assert participants[1].user_id is None
    assert participants[1].role == "client"


def test_envelope_parse_payload_validates_original_against_model() -> None:
    envelope = EventEnvelope.model_validate(
        {
            "original": {
                "booking_id": "b-1",
                "trigger_event": "BOOKING_CREATED",
                "recipients": [{"email": "cli@example.com", "role": "client"}],
                "template_data": {"title": "Session"},
            },
            "normalized": {"participants": []},
        }
    )

    payload = envelope.parse_payload(NotificationCommandPayload)

    assert payload.booking_id == "b-1"
    assert payload.recipients[0].email == "cli@example.com"
    assert payload.template_data == {"title": "Session"}


def test_envelope_participant_carries_optional_locale() -> None:
    envelope = EventEnvelope.model_validate(
        {
            "original": {},
            "normalized": {
                "participants": [
                    {"email": "org@example.com", "role": "organizer", "locale": "ru"},
                    {"email": "cli@example.com", "role": "client"},
                ]
            },
        }
    )

    participants = envelope.normalized.participants
    assert participants[0].locale == "ru"
    assert participants[1].locale is None


def test_envelope_defaults_when_sections_missing() -> None:
    envelope = EventEnvelope.model_validate({})

    assert envelope.original == {}
    assert envelope.normalized.participants == []
