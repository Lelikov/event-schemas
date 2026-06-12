"""Booking event payload schemas (the ``original`` section of the envelope)."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from event_schemas.types import ClientInfo, TimeZoneName, UserInfo, UuidStr


class BookingParticipant(BaseModel):
    """A participant entry in the ``users`` list of booking lifecycle payloads."""

    email: EmailStr = Field(..., description="Participant email address")
    role: str | None = Field(None, description="organizer | client | previous_organizer")
    time_zone: TimeZoneName | None = Field(None, description="IANA time zone, if known")
    locale: str | None = Field(None, description="Preferred language tag (e.g. 'ru', 'en'), if known")

    model_config = {"json_schema_extra": {"example": {"email": "organizer@example.com", "role": "organizer"}}}


class BookingCreatedPayload(BaseModel):
    """Payload for booking.created event."""

    volunteer_id: UuidStr | None = Field(None, description="Organizer (volunteer) UUID")
    client_id: UuidStr | None = Field(None, description="Client UUID")
    user: UserInfo = Field(..., description="Organizer information")
    client: ClientInfo = Field(..., description="Client information")
    start_time: datetime = Field(..., description="Booking start time (ISO 8601)")
    end_time: datetime = Field(..., description="Booking end time (ISO 8601)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "volunteer_id": "550e8400-e29b-41d4-a716-446655440001",
                "client_id": "550e8400-e29b-41d4-a716-446655440002",
                "user": {"email": "organizer@example.com"},
                "client": {"email": "client@example.com"},
                "start_time": "2024-03-01T10:00:00Z",
                "end_time": "2024-03-01T11:00:00Z",
            }
        }
    }


class BookingRescheduledPayload(BaseModel):
    """Payload for booking.rescheduled event.

    cal.com mints a NEW booking uid on reschedule: the CloudEvent ``bookingid``
    attribute carries the NEW uid, ``previous_booking_uid`` carries the old one
    (cal.com ``rescheduleUid``) so consumers can link booking identities.
    """

    users: list[BookingParticipant] = Field(default_factory=list, description="Organizer and client")
    start_time: datetime = Field(..., description="New booking start time")
    end_time: datetime = Field(..., description="New booking end time")
    previous_start_time: datetime | None = Field(None, description="Previous booking start time")
    previous_booking_uid: str | None = Field(None, description="Old booking uid (cal.com rescheduleUid)")
    rescheduled_by: str | None = Field(None, description="Email of the actor who rescheduled")

    model_config = {
        "json_schema_extra": {
            "example": {
                "users": [
                    {"email": "organizer@example.com", "role": "organizer"},
                    {"email": "client@example.com", "role": "client"},
                ],
                "start_time": "2024-03-02T10:00:00Z",
                "end_time": "2024-03-02T11:00:00Z",
                "previous_start_time": "2024-03-01T10:00:00Z",
                "previous_booking_uid": "xaYwx8FnWLR2ZSvT8vg4WA",
                "rescheduled_by": "organizer@example.com",
            }
        }
    }


class BookingReassignedPayload(BaseModel):
    """Payload for booking.reassigned event."""

    users: list[BookingParticipant] = Field(
        default_factory=list,
        description="New organizer, client and previous_organizer entries",
    )
    previous_organizer_email: EmailStr | None = Field(None, description="Email of the previous organizer")

    model_config = {
        "json_schema_extra": {
            "example": {
                "users": [
                    {"email": "new.organizer@example.com", "role": "organizer"},
                    {"email": "client@example.com", "role": "client"},
                    {"email": "old.organizer@example.com", "role": "previous_organizer"},
                ],
                "previous_organizer_email": "old.organizer@example.com",
            }
        }
    }


class BookingCancelledPayload(BaseModel):
    """Payload for booking.cancelled event."""

    users: list[BookingParticipant] = Field(default_factory=list, description="Organizer and client")
    cancellation_reason: str | None = Field(None, description="Reason for cancellation")
    cancelled_by: str | None = Field(None, description="Email of the actor who cancelled")

    model_config = {
        "json_schema_extra": {
            "example": {
                "users": [
                    {"email": "organizer@example.com", "role": "organizer"},
                    {"email": "client@example.com", "role": "client"},
                ],
                "cancellation_reason": "Client request",
                "cancelled_by": "client@example.com",
            }
        }
    }


class BookingReminderSentPayload(BaseModel):
    """Payload for booking.reminder_sent event (no producer today; kept for saver routing)."""

    client_id: UuidStr | None = Field(None, description="Client UUID")
    email: EmailStr = Field(..., description="Email address where reminder was sent")

    model_config = {
        "json_schema_extra": {
            "example": {
                "client_id": "550e8400-e29b-41d4-a716-446655440002",
                "email": "client@example.com",
            }
        }
    }


class BookingRejectedPayload(BaseModel):
    """Payload for booking.rejected event."""

    client_email: EmailStr = Field(..., description="Client email address")
    rejection_type: str | None = Field(None, description="Type: month_limit, year_limit, min_interval, blacklisted")
    rejection_reasons: list[str] = Field(default_factory=list, description="Human-readable rejection reasons")
    available_from: datetime | None = Field(None, description="Earliest available booking time")
    has_active_booking: bool = Field(False, description="Whether client has an active future booking")
    active_booking_start: datetime | None = Field(None, description="Start time of the active booking if exists")

    model_config = {
        "json_schema_extra": {
            "example": {
                "client_email": "client@example.com",
                "rejection_type": "month_limit",
                "rejection_reasons": ["Monthly booking limit reached"],
                "available_from": "2024-04-01T00:00:00Z",
                "has_active_booking": False,
                "active_booking_start": None,
            }
        }
    }
