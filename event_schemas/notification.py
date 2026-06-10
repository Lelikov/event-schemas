"""Notification event payload schemas."""

from typing import Any

from pydantic import BaseModel, EmailStr, Field

from event_schemas.types import RecipientRole, TriggerEvent


class EmailNotificationPayload(BaseModel):
    """Payload for notification.email.message_sent event (standard case)."""

    email: EmailStr = Field(..., description="Recipient email address")
    job_id: str | None = Field(None, description="UniSender job ID")
    recipient_role: RecipientRole = Field(..., description="Recipient role (organizer or client)")
    trigger_event: TriggerEvent = Field(..., description="Event that triggered this notification")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "client@example.com",
                "job_id": "job_123",
                "recipient_role": "client",
                "trigger_event": "BOOKING_CREATED",
            }
        }
    }


class TelegramNotificationPayload(BaseModel):
    """Payload for notification.telegram.message_sent event."""

    email: EmailStr = Field(..., description="Recipient email address (organizer)")
    recipient_role: RecipientRole = Field(
        default=RecipientRole.ORGANIZER,
        description="Recipient role (currently only organizer)",
    )
    trigger_event: TriggerEvent = Field(..., description="Event that triggered this notification")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "organizer@example.com",
                "recipient_role": "organizer",
                "trigger_event": "BOOKING_CREATED",
            }
        }
    }


class NotificationRecipient(BaseModel):
    """Single recipient for a notification command."""

    email: EmailStr = Field(..., description="Recipient email address")
    role: RecipientRole = Field(..., description="Recipient role in booking context")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "organizer@example.com",
                "role": "organizer",
            }
        }
    }


class NotificationCommandPayload(BaseModel):
    """Payload for notification.send_requested event.

    Published by the booking service to request notifications.
    event-notifier consumes this and dispatches via appropriate channels.
    """

    booking_id: str = Field(..., description="Booking UID to associate notifications with")
    trigger_event: TriggerEvent = Field(..., description="Booking lifecycle event that triggered this")
    recipients: list[NotificationRecipient] = Field(..., description="List of recipients to notify")
    template_data: dict[str, Any] = Field(
        default_factory=dict,
        description="Extra key-value data for template rendering (e.g. booking_start, organizer_name)",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "booking_id": "booking-uuid-123",
                "trigger_event": "BOOKING_CREATED",
                "recipients": [
                    {"email": "organizer@example.com", "role": "organizer"},
                    {"email": "client@example.com", "role": "client"},
                ],
                "template_data": {
                    "booking_start": "2026-05-01T10:00:00Z",
                    "organizer_name": "Jane Smith",
                },
            }
        }
    }


class PushNotificationPayload(BaseModel):
    """Payload for notification.push.message_sent event (delivery confirmation)."""

    email: EmailStr = Field(..., description="Recipient email address")
    recipient_role: RecipientRole = Field(..., description="Recipient role")
    trigger_event: TriggerEvent = Field(..., description="Event that triggered this notification")
    device_token: str = Field(..., description="FCM/APNS device token used")
    message_id: str | None = Field(None, description="Provider message ID for tracking")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "client@example.com",
                "recipient_role": "client",
                "trigger_event": "BOOKING_CREATED",
                "device_token": "fcm-token-abc123",
                "message_id": "projects/my-project/messages/abc123",
            }
        }
    }
