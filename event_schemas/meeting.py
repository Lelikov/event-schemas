"""Meeting event payload schemas."""

from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field

from event_schemas.types import RecipientRole


class MeetingUrlCreatedPayload(BaseModel):
    """Payload for meeting.url_created event."""

    email: EmailStr = Field(..., description="Recipient email address")
    recipient_role: RecipientRole = Field(..., description="Recipient role (organizer or client)")
    meeting_url: AnyHttpUrl = Field(..., description="Meeting URL (Jitsi, Zoom, etc.)")

    model_config = {"json_schema_extra": {"example": {
        "email": "organizer@example.com",
        "recipient_role": "organizer",
        "meeting_url": "https://meet.jit.si/booking-123",
    }}}


class MeetingUrlDeletedPayload(BaseModel):
    """Payload for meeting.url_deleted event."""

    recipient_role: RecipientRole = Field(..., description="Recipient role (organizer or client)")

    model_config = {"json_schema_extra": {"example": {"recipient_role": "organizer"}}}
