"""Core types and enums for event schemas."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class EventType(str, Enum):
    """Unified event types across all services."""

    # Booking lifecycle
    BOOKING_CREATED = "booking.created"
    BOOKING_RESCHEDULED = "booking.rescheduled"
    BOOKING_REASSIGNED = "booking.reassigned"
    BOOKING_CANCELLED = "booking.cancelled"
    BOOKING_REMINDER_SENT = "booking.reminder_sent"

    # Chat lifecycle
    CHAT_CREATED = "chat.created"
    CHAT_DELETED = "chat.deleted"
    CHAT_MESSAGE_SENT = "chat.message_sent"

    # Meeting
    MEETING_URL_CREATED = "meeting.url_created"
    MEETING_URL_DELETED = "meeting.url_deleted"

    # Notifications
    NOTIFICATION_EMAIL_SENT = "notification.email.message_sent"
    NOTIFICATION_TELEGRAM_SENT = "notification.telegram.message_sent"

    # External integrations
    UNISENDER_STATUS_CREATED = "unisender.events.v1.transactional.status.create"
    GETSTREAM_MESSAGE_NEW = "getstream.events.v1.message.new"
    GETSTREAM_MESSAGE_UPDATED = "getstream.events.v1.message.updated"
    GETSTREAM_MESSAGE_DELETED = "getstream.events.v1.message.deleted"
    GETSTREAM_MESSAGE_READ = "getstream.events.v1.message.read"
    JITSI_ROOM_CREATED = "jitsi.room.created"
    JITSI_PARTICIPANT_JOINED = "jitsi.participant.joined"
    JITSI_PARTICIPANT_LEFT = "jitsi.participant.left"


class EventPriority(int, Enum):
    """Event priority levels for RabbitMQ priority queues."""

    CRITICAL = 10  # booking lifecycle events
    HIGH = 7  # notifications
    NORMAL = 5  # chat messages, status updates
    LOW = 1  # analytics, audit events


class RecipientRole(str, Enum):
    """Recipient role in booking context."""

    ORGANIZER = "organizer"
    CLIENT = "client"


class TriggerEvent(str, Enum):
    """Event that triggered a notification."""

    BOOKING_CREATED = "BOOKING_CREATED"
    BOOKING_RESCHEDULED = "BOOKING_RESCHEDULED"
    BOOKING_REASSIGNED = "BOOKING_REASSIGNED"
    BOOKING_CANCELLED = "BOOKING_CANCELLED"
    BOOKING_REMINDER = "BOOKING_REMINDER"
    BOOKING_REJECTED = "BOOKING_REJECTED"


class UserInfo(BaseModel):
    """User information (organizer or client)."""

    email: EmailStr
    time_zone: str = Field(
        ...,
        pattern=r"^(UTC|[A-Za-z_]+/[A-Za-z_]+)$",
        description="IANA timezone (e.g., UTC, Europe/Moscow)",
    )


class ClientInfo(BaseModel):
    """Client information (extends UserInfo for future fields)."""

    email: EmailStr
    time_zone: str = Field(
        ...,
        pattern=r"^(UTC|[A-Za-z_]+/[A-Za-z_]+)$",
        description="IANA timezone (e.g., UTC, Europe/Moscow)",
    )


# Event type to priority mapping
EVENT_PRIORITIES: dict[EventType, EventPriority] = {
    # Critical: booking lifecycle
    EventType.BOOKING_CREATED: EventPriority.CRITICAL,
    EventType.BOOKING_RESCHEDULED: EventPriority.CRITICAL,
    EventType.BOOKING_REASSIGNED: EventPriority.CRITICAL,
    EventType.BOOKING_CANCELLED: EventPriority.CRITICAL,
    # High: notifications
    EventType.NOTIFICATION_EMAIL_SENT: EventPriority.HIGH,
    EventType.NOTIFICATION_TELEGRAM_SENT: EventPriority.HIGH,
    EventType.BOOKING_REMINDER_SENT: EventPriority.HIGH,
    # Normal: chat and meeting
    EventType.CHAT_CREATED: EventPriority.NORMAL,
    EventType.CHAT_DELETED: EventPriority.NORMAL,
    EventType.CHAT_MESSAGE_SENT: EventPriority.NORMAL,
    EventType.MEETING_URL_CREATED: EventPriority.NORMAL,
    EventType.MEETING_URL_DELETED: EventPriority.NORMAL,
    # Normal: external integrations
    EventType.UNISENDER_STATUS_CREATED: EventPriority.NORMAL,
    EventType.GETSTREAM_MESSAGE_NEW: EventPriority.NORMAL,
    EventType.GETSTREAM_MESSAGE_UPDATED: EventPriority.NORMAL,
    EventType.GETSTREAM_MESSAGE_DELETED: EventPriority.NORMAL,
    EventType.GETSTREAM_MESSAGE_READ: EventPriority.NORMAL,
    EventType.JITSI_ROOM_CREATED: EventPriority.NORMAL,
    EventType.JITSI_PARTICIPANT_JOINED: EventPriority.NORMAL,
    EventType.JITSI_PARTICIPANT_LEFT: EventPriority.NORMAL,
}

# Event type to schema version mapping
EVENT_SCHEMA_VERSIONS: dict[EventType, str] = {
    # All events start at v1
    EventType.BOOKING_CREATED: "v1",
    EventType.BOOKING_RESCHEDULED: "v1",
    EventType.BOOKING_REASSIGNED: "v1",
    EventType.BOOKING_CANCELLED: "v1",
    EventType.BOOKING_REMINDER_SENT: "v1",
    EventType.CHAT_CREATED: "v1",
    EventType.CHAT_DELETED: "v1",
    EventType.CHAT_MESSAGE_SENT: "v1",
    EventType.MEETING_URL_CREATED: "v1",
    EventType.MEETING_URL_DELETED: "v1",
    EventType.NOTIFICATION_EMAIL_SENT: "v1",
    EventType.NOTIFICATION_TELEGRAM_SENT: "v1",
    EventType.UNISENDER_STATUS_CREATED: "v1",
    EventType.GETSTREAM_MESSAGE_NEW: "v1",
    EventType.GETSTREAM_MESSAGE_UPDATED: "v1",
    EventType.GETSTREAM_MESSAGE_DELETED: "v1",
    EventType.GETSTREAM_MESSAGE_READ: "v1",
    EventType.JITSI_ROOM_CREATED: "v1",
    EventType.JITSI_PARTICIPANT_JOINED: "v1",
    EventType.JITSI_PARTICIPANT_LEFT: "v1",
}
