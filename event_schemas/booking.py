"""Booking event payload schemas."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from event_schemas.types import ClientInfo, UserInfo


class BookingCreatedPayload(BaseModel):
    """Payload for booking.created event."""

    user: UserInfo = Field(..., description="Organizer information")
    client: ClientInfo = Field(..., description="Client information")
    start_time: datetime = Field(..., description="Booking start time (ISO 8601)")
    end_time: datetime = Field(..., description="Booking end time (ISO 8601)")

    model_config = {"json_schema_extra": {"example": {
        "user": {"email": "organizer@example.com", "time_zone": "Europe/Moscow"},
        "client": {"email": "client@example.com", "time_zone": "UTC"},
        "start_time": "2024-03-01T10:00:00Z",
        "end_time": "2024-03-01T11:00:00Z",
    }}}


class BookingRescheduledPayload(BaseModel):
    """Payload for booking.rescheduled event."""

    start_time: datetime = Field(..., description="New booking start time")
    end_time: datetime = Field(..., description="New booking end time")
    previous_booking: dict[str, datetime | None] = Field(
        default_factory=dict,
        description="Previous booking details",
    )

    model_config = {"json_schema_extra": {"example": {
        "start_time": "2024-03-02T10:00:00Z",
        "end_time": "2024-03-02T11:00:00Z",
        "previous_booking": {"start_time": "2024-03-01T10:00:00Z"},
    }}}


class BookingReassignedPayload(BaseModel):
    """Payload for booking.reassigned event."""

    previous_organizer: dict[str, str | None] = Field(
        default_factory=dict,
        description="Previous organizer information",
    )
    user: UserInfo = Field(..., description="New organizer information")

    model_config = {"json_schema_extra": {"example": {
        "previous_organizer": {"email": "old.organizer@example.com"},
        "user": {"email": "new.organizer@example.com", "time_zone": "Europe/Moscow"},
    }}}


class BookingCancelledPayload(BaseModel):
    """Payload for booking.cancelled event."""

    cancellation_reason: str | None = Field(None, description="Reason for cancellation")

    model_config = {"json_schema_extra": {"example": {"cancellation_reason": "Client request"}}}


class BookingReminderSentPayload(BaseModel):
    """Payload for booking.reminder_sent event."""

    email: EmailStr = Field(..., description="Email address where reminder was sent")

    model_config = {"json_schema_extra": {"example": {"email": "client@example.com"}}}
