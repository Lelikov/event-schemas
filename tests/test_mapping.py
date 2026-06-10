"""Tests for EventType -> payload model mapping and payload contracts."""

from datetime import UTC, datetime

from pydantic import BaseModel

from event_schemas.attributes import BOOKING_ID_ATTRIBUTE, BOOKING_ID_HEADER
from event_schemas.booking import BookingRejectedPayload, BookingRescheduledPayload
from event_schemas.mapping import PAYLOAD_MODELS
from event_schemas.meeting import MeetingUrlCreatedPayload
from event_schemas.types import EventType


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
