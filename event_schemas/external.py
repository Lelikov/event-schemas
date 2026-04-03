"""External integration event payload schemas (UniSender, GetStream, Jitsi)."""

from typing import Any

from pydantic import BaseModel, Field


class UniSenderStatusPayload(BaseModel):
    """Payload for unisender.events.v1.transactional.status.create event.

    This is a wrapper around UniSender Go webhook payload after extraction.
    """

    # UniSender event fields (simplified, extend as needed)
    event_name: str | None = Field(None, description="UniSender event name")
    event_data: dict[str, Any] = Field(default_factory=dict, description="UniSender event data")

    model_config = {"json_schema_extra": {"example": {
        "event_name": "transactional_email_status",
        "event_data": {
            "email": "recipient@example.com",
            "status": "sent",
            "job_id": "job_123",
        },
    }}}


class GetStreamEventPayload(BaseModel):
    """Payload for getstream.events.v1.*.create events.

    GetStream webhook payload (pass-through, minimal validation).
    """

    type: str = Field(..., description="GetStream event type (message.new, message.updated, etc.)")
    channel_id: str | None = Field(None, description="Channel ID (booking_id)")
    user: dict[str, Any] | None = Field(None, description="User who triggered the event")
    message: dict[str, Any] | None = Field(None, description="Message object (for message events)")
    # Allow additional fields
    extra: dict[str, Any] = Field(default_factory=dict, description="Additional GetStream fields")

    model_config = {
        "extra": "allow",
        "json_schema_extra": {"example": {
            "type": "message.new",
            "channel_id": "booking-123",
            "user": {"id": "user_123", "role": "user"},
            "message": {"id": "msg_456", "text": "Hello"},
        }},
    }


class JitsiEventPayload(BaseModel):
    """Payload for jitsi.* events.

    Jitsi webhook payload (pass-through, minimal validation).
    JWT claims are merged into data by event-receiver.
    """

    room: str | None = Field(None, description="Jitsi room name (booking_id)")
    event_type: str | None = Field(None, description="Jitsi event type")
    # Allow additional fields from JWT claims
    extra: dict[str, Any] = Field(default_factory=dict, description="Additional Jitsi/JWT fields")

    model_config = {
        "extra": "allow",
        "json_schema_extra": {"example": {
            "room": "booking-123",
            "event_type": "room.created",
            "participant_id": "user_456",
        }},
    }
