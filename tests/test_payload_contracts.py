"""Contract completeness and wire-format fidelity tests.

Covers: every EventType has a payload model, a priority and a schema version;
every payload model's documented example round-trips through the canonical
envelope JSON wire format; field validators (IANA time zone, UUID strings).
"""

import json

import pytest
from pydantic import ValidationError

from event_schemas.booking import BookingCreatedPayload, BookingParticipant, BookingReminderSentPayload
from event_schemas.envelope import EventEnvelope
from event_schemas.mapping import PAYLOAD_MODELS
from event_schemas.notification import NotificationRecipient
from event_schemas.types import EVENT_PRIORITIES, EVENT_SCHEMA_VERSIONS, EventType, UserInfo
from event_schemas.user import BookingClientReassignedPayload, UserEmailChangeRequestedPayload

# --- EventType <-> PAYLOAD_MODELS / priorities / versions completeness ---


def test_every_event_type_has_priority() -> None:
    missing = [t for t in EventType if t not in EVENT_PRIORITIES]

    assert missing == [], f"EventTypes without priority: {missing}"


def test_every_event_type_has_schema_version() -> None:
    missing = [t for t in EventType if t not in EVENT_SCHEMA_VERSIONS]

    assert missing == [], f"EventTypes without schema version: {missing}"


def test_no_orphan_entries_in_contract_maps() -> None:
    event_types = set(EventType)

    assert set(PAYLOAD_MODELS) <= event_types
    assert set(EVENT_PRIORITIES) <= event_types
    assert set(EVENT_SCHEMA_VERSIONS) <= event_types


def test_every_payload_model_has_documented_example() -> None:
    missing = [
        event_type
        for event_type, model in PAYLOAD_MODELS.items()
        if not (model.model_config.get("json_schema_extra") or {}).get("example")
    ]

    assert missing == [], f"Payload models without json_schema_extra example: {missing}"


# --- Wire-format fidelity: envelope JSON round-trip for every event type ---


@pytest.mark.parametrize("event_type", list(PAYLOAD_MODELS), ids=lambda t: t.value)
def test_envelope_round_trip_for_every_event_type(event_type: EventType) -> None:
    """Each model's documented example survives JSON wire encoding inside the canonical envelope."""
    model = PAYLOAD_MODELS[event_type]
    example = model.model_config["json_schema_extra"]["example"]  # type: ignore[index]
    wire = json.dumps(
        {
            "original": example,
            "normalized": {"participants": [{"email": "org@example.com", "role": "organizer"}]},
        }
    )

    envelope = EventEnvelope.model_validate_json(wire)
    payload = envelope.parse_payload(model)

    redumped = json.loads(payload.model_dump_json(exclude_unset=True))
    reparsed = model.model_validate(redumped)
    assert reparsed == payload
    assert envelope.normalized.participants[0].email == "org@example.com"


# --- IANA time zone validation ---


def test_user_info_accepts_valid_iana_time_zone() -> None:
    info = UserInfo(email="org@example.com", time_zone="Europe/Madrid")

    assert info.time_zone == "Europe/Madrid"


def test_user_info_rejects_invalid_time_zone() -> None:
    with pytest.raises(ValidationError, match="IANA time zone"):
        UserInfo(email="org@example.com", time_zone="Mars/Olympus_Mons")


def test_booking_participant_rejects_utc_offset_as_time_zone() -> None:
    with pytest.raises(ValidationError, match="IANA time zone"):
        BookingParticipant(email="org@example.com", time_zone="UTC+3")


def test_booking_participant_time_zone_optional() -> None:
    participant = BookingParticipant(email="org@example.com")

    assert participant.time_zone is None


def test_booking_participant_locale_optional() -> None:
    assert BookingParticipant(email="org@example.com").locale is None
    assert BookingParticipant(email="org@example.com", locale="ru").locale == "ru"


def test_notification_recipient_locale_optional() -> None:
    assert NotificationRecipient(email="cli@example.com", role="client").locale is None
    assert NotificationRecipient(email="cli@example.com", role="client", locale="en").locale == "en"


# --- UUID string validation ---


def test_booking_created_accepts_uuid_ids() -> None:
    payload = BookingCreatedPayload.model_validate(BookingCreatedPayload.model_config["json_schema_extra"]["example"])

    assert payload.volunteer_id == "550e8400-e29b-41d4-a716-446655440001"
    assert payload.client_id == "550e8400-e29b-41d4-a716-446655440002"


def test_booking_created_rejects_non_uuid_ids() -> None:
    example = dict(BookingCreatedPayload.model_config["json_schema_extra"]["example"])  # type: ignore[arg-type]
    example["volunteer_id"] = "not-a-uuid"

    with pytest.raises(ValidationError, match="not a valid UUID"):
        BookingCreatedPayload.model_validate(example)


def test_booking_created_ids_remain_optional() -> None:
    payload = BookingCreatedPayload(
        user={"email": "org@example.com"},
        client={"email": "cli@example.com"},
        start_time="2026-05-01T10:00:00Z",
        end_time="2026-05-01T11:00:00Z",
    )

    assert payload.volunteer_id is None
    assert payload.client_id is None


def test_reminder_sent_rejects_non_uuid_client_id() -> None:
    with pytest.raises(ValidationError, match="not a valid UUID"):
        BookingReminderSentPayload(client_id="42", email="cli@example.com")


def test_user_email_change_requires_uuid_user_id() -> None:
    with pytest.raises(ValidationError, match="not a valid UUID"):
        UserEmailChangeRequestedPayload(
            user_id="client-42",
            old_email="old@example.com",
            new_email="new@example.com",
            requested_by="admin@example.com",
        )


def test_client_reassigned_requires_uuid_new_client_user_id() -> None:
    with pytest.raises(ValidationError, match="not a valid UUID"):
        BookingClientReassignedPayload(
            booking_uid="book-123",
            new_client_user_id="client-42",
            requested_by="admin@example.com",
        )
