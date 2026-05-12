"""Booking event payload schemas."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from event_schemas.types import ClientInfo, UserInfo


class BookingCreatedPayload(BaseModel):
    """Payload for booking.created event."""

    volunteer_id: str | None = Field(None, description="Organizer (volunteer) UUID")
    client_id: str | None = Field(None, description="Client UUID")
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
    """Payload for booking.rescheduled event."""

    volunteer_id: str = Field(..., description="Organizer (volunteer) UUID")
    client_id: str = Field(..., description="Client UUID")
    start_time: datetime = Field(..., description="New booking start time")
    end_time: datetime = Field(..., description="New booking end time")
    previous_booking: dict[str, datetime | None] = Field(
        default_factory=dict,
        description="Previous booking details",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "volunteer_id": "550e8400-e29b-41d4-a716-446655440001",
                "client_id": "550e8400-e29b-41d4-a716-446655440002",
                "start_time": "2024-03-02T10:00:00Z",
                "end_time": "2024-03-02T11:00:00Z",
                "previous_booking": {"start_time": "2024-03-01T10:00:00Z"},
            }
        }
    }


class BookingReassignedPayload(BaseModel):
    """Payload for booking.reassigned event."""

    volunteer_id: str = Field(..., description="New organizer (volunteer) UUID")
    client_id: str = Field(..., description="Client UUID")
    previous_organizer: dict[str, str | None] = Field(
        default_factory=dict,
        description="Previous organizer information",
    )
    user: UserInfo = Field(..., description="New organizer information")

    model_config = {
        "json_schema_extra": {
            "example": {
                "volunteer_id": "550e8400-e29b-41d4-a716-446655440003",
                "client_id": "550e8400-e29b-41d4-a716-446655440002",
                "previous_organizer": {"email": "old.organizer@example.com"},
                "user": {"email": "new.organizer@example.com"},
            }
        }
    }


class BookingCancelledPayload(BaseModel):
    """Payload for booking.cancelled event."""

    volunteer_id: str = Field(..., description="Organizer (volunteer) UUID")
    client_id: str = Field(..., description="Client UUID")
    cancellation_reason: str | None = Field(None, description="Reason for cancellation")

    model_config = {
        "json_schema_extra": {
            "example": {
                "volunteer_id": "550e8400-e29b-41d4-a716-446655440001",
                "client_id": "550e8400-e29b-41d4-a716-446655440002",
                "cancellation_reason": "Client request",
            }
        }
    }


class BookingReminderSentPayload(BaseModel):
    """Payload for booking.reminder_sent event."""

    client_id: str = Field(..., description="Client UUID")
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
    rejection_type: str | None = Field(None, description="Type: month_limit, year_limit, min_interval")
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
