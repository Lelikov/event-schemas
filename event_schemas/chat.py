"""Chat event payload schemas (the ``original`` section of the envelope)."""

from pydantic import BaseModel, Field


class ChatCreatedPayload(BaseModel):
    """Payload for chat.created event (published by event-booking after GetStream channel creation)."""

    channel_id: str = Field(..., description="GetStream channel id (== booking uid)")

    model_config = {"json_schema_extra": {"example": {"channel_id": "n3FHda8Cpy48QW4JZX9th7"}}}


class ChatDeletedPayload(BaseModel):
    """Payload for chat.deleted event."""

    channel_id: str = Field(..., description="GetStream channel id (== booking uid)")

    model_config = {"json_schema_extra": {"example": {"channel_id": "n3FHda8Cpy48QW4JZX9th7"}}}


class ChatMessageSentPayload(BaseModel):
    """Payload for chat.message_sent event."""

    user_id: str = Field(..., description="GetStream user ID who sent the message")

    model_config = {"json_schema_extra": {"example": {"user_id": "user_123"}}}
