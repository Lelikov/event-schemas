"""Chat event payload schemas."""

from pydantic import BaseModel, Field


class ChatCreatedPayload(BaseModel):
    """Payload for chat.created event."""

    organizer_id: str = Field(..., description="GetStream user ID of organizer")
    client_id: str = Field(..., description="GetStream user ID of client")

    model_config = {"json_schema_extra": {"example": {
        "organizer_id": "user_123",
        "client_id": "user_456",
    }}}


class ChatDeletedPayload(BaseModel):
    """Payload for chat.deleted event."""

    # Empty payload - booking_id in CloudEvent attributes is sufficient
    model_config = {"json_schema_extra": {"example": {}}}


class ChatMessageSentPayload(BaseModel):
    """Payload for chat.message_sent event."""

    user_id: str = Field(..., description="GetStream user ID who sent the message")

    model_config = {"json_schema_extra": {"example": {"user_id": "user_123"}}}
