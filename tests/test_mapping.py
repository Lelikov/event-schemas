"""Tests for EventType -> payload model mapping and payload contracts."""

from datetime import UTC, datetime

from pydantic import BaseModel

from event_schemas.attributes import BOOKING_ID_ATTRIBUTE, BOOKING_ID_HEADER
from event_schemas.booking import BookingRejectedPayload, BookingRescheduledPayload
from event_schemas.mapping import PAYLOAD_MODELS
from event_schemas.meeting import MeetingUrlCreatedPayload
from event_schemas.notification import NotificationCommandPayload
from event_schemas.types import EventType, TriggerEvent


def test_every_event_type_has_a_payload_model() -> None:
    missing = [t for t in EventType if t not in PAYLOAD_MODELS]

    assert missing == [], f"EventTypes without payload models: {missing}"


def test_all_mapped_models_are_pydantic_models() -> None:
    for event_type, model in PAYLOAD_MODELS.items():
        assert issubclass(model, BaseModel), event_type


def test_booking_rescheduled_carries_previous_booking_uid() -> None:
    payload = BookingRescheduledPayload(
        users=[{"email": "org@example.com", "role": "organizer"}],
        start_time=datetime(2026, 5, 13, 10, 0, tzinfo=UTC),
        end_time=datetime(2026, 5, 13, 11, 0, tzinfo=UTC),
        previous_start_time=datetime(2026, 5, 12, 10, 0, tzinfo=UTC),
        previous_booking_uid="xaYwx8FnWLR2ZSvT8vg4WA",
    )

    assert payload.previous_booking_uid == "xaYwx8FnWLR2ZSvT8vg4WA"


def test_booking_rejected_requires_client_email() -> None:
    payload = BookingRejectedPayload(
        client_email="cli@example.com",
        rejection_type="month_limit",
        rejection_reasons=["Monthly booking limit reached"],
    )

    assert payload.client_email == "cli@example.com"
    assert payload.has_active_booking is False


def test_booking_rejected_accepts_blacklisted_type() -> None:
    payload = BookingRejectedPayload(
        client_email="cli@example.com",
        rejection_type="blacklisted",
        rejection_reasons=["Client is blacklisted"],
    )

    assert payload.rejection_type == "blacklisted"


def test_trigger_event_has_blacklisted_rejection() -> None:
    assert TriggerEvent.BOOKING_REJECTED_BLACKLISTED == "BOOKING_REJECTED_BLACKLISTED"

    payload = NotificationCommandPayload(
        booking_id="booking-uuid-123",
        trigger_event=TriggerEvent.BOOKING_REJECTED_BLACKLISTED,
        recipients=[{"email": "cli@example.com", "role": "client", "locale": "ru"}],
    )

    assert payload.trigger_event is TriggerEvent.BOOKING_REJECTED_BLACKLISTED


def test_meeting_url_created_matches_consumer_contract() -> None:
    payload = MeetingUrlCreatedPayload(
        email="org@example.com",
        recipient_role="organizer",
        meeting_url="https://meet.example.com/abc",
    )

    assert str(payload.meeting_url) == "https://meet.example.com/abc"


def test_booking_id_attribute_has_no_underscore() -> None:
    assert BOOKING_ID_ATTRIBUTE == "bookingid"
    assert BOOKING_ID_HEADER == "ce-bookingid"
