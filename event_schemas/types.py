"""Core types and enums for event schemas."""

from enum import Enum, StrEnum

from pydantic import BaseModel, EmailStr


class SourceType(StrEnum):
    """Event source identifiers."""

    ADMIN = "admin"
    BOOKING = "booking"
    GETSTREAM = "getstream"
    UNISENDER_GO = "unisender-go"
    JITSI = "jitsi"


class EventType(str, Enum):
    """Unified event types across all services."""

    # Booking lifecycle
    BOOKING_CREATED = "booking.created"
    BOOKING_RESCHEDULED = "booking.rescheduled"
    BOOKING_REASSIGNED = "booking.reassigned"
    BOOKING_CANCELLED = "booking.cancelled"
    BOOKING_REMINDER_SENT = "booking.reminder_sent"
    BOOKING_CLIENT_REASSIGNED = "booking.client_reassigned"
    BOOKING_REJECTED = "booking.rejected"

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
    NOTIFICATION_SEND_REQUESTED = "notification.send_requested"
    NOTIFICATION_PUSH_SENT = "notification.push.message_sent"

    # User management
    USER_EMAIL_CHANGE_REQUESTED = "user.email.change_requested"

    # External integrations
    UNISENDER_STATUS_CREATED = "unisender.events.v1.transactional.status.create"
    GETSTREAM_CHANNEL_CREATED = "getstream.channel.created"
    GETSTREAM_CHANNEL_DELETED = "getstream.channel.deleted"
    GETSTREAM_MESSAGE_NEW = "getstream.message.new"
    GETSTREAM_MESSAGE_UPDATED = "getstream.message.updated"
    GETSTREAM_MESSAGE_DELETED = "getstream.message.deleted"
    GETSTREAM_MESSAGE_READ = "getstream.message.read"
    JITSI_CONFERENCE_JOINED = "jitsi.conference.joined"
    JITSI_CONFERENCE_LEFT = "jitsi.conference.left"
    JITSI_PARTICIPANT_JOINED = "jitsi.participant.joined"
    JITSI_PARTICIPANT_LEFT = "jitsi.participant.left"
    JITSI_PARTICIPANT_MUTED = "jitsi.participant.muted"
    JITSI_PARTICIPANT_MENU_BUTTON_CLICK = "jitsi.participant.menu_button_click"
    JITSI_AUDIO_MUTE_STATUS_CHANGED = "jitsi.audio.mute_status_changed"
    JITSI_VIDEO_MUTE_STATUS_CHANGED = "jitsi.video.mute_status_changed"
    JITSI_SPEAKER_DOMINANT_CHANGED = "jitsi.speaker.dominant_changed"
    JITSI_DEVICE_LIST_CHANGED = "jitsi.device.list_changed"
    JITSI_CAMERA_ERROR = "jitsi.camera.error"
    JITSI_MIC_ERROR = "jitsi.mic.error"
    JITSI_ERROR_OCCURRED = "jitsi.error.occurred"
    JITSI_PEER_CONNECTION_FAILURE = "jitsi.peer_connection.failure"
    JITSI_SUSPEND_DETECTED = "jitsi.suspend.detected"
    JITSI_TOOLBAR_BUTTON_CLICKED = "jitsi.toolbar.button_clicked"


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
    time_zone: str | None = None


class ClientInfo(UserInfo):
    """Client information (extends UserInfo; inherits email and time_zone)."""


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
    EventType.NOTIFICATION_SEND_REQUESTED: EventPriority.HIGH,
    EventType.NOTIFICATION_PUSH_SENT: EventPriority.HIGH,
    EventType.BOOKING_REMINDER_SENT: EventPriority.HIGH,
    EventType.BOOKING_CLIENT_REASSIGNED: EventPriority.CRITICAL,
    EventType.BOOKING_REJECTED: EventPriority.CRITICAL,
    # Critical: user management
    EventType.USER_EMAIL_CHANGE_REQUESTED: EventPriority.CRITICAL,
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
    EventType.GETSTREAM_CHANNEL_CREATED: EventPriority.NORMAL,
    EventType.GETSTREAM_CHANNEL_DELETED: EventPriority.NORMAL,
    EventType.JITSI_CONFERENCE_JOINED: EventPriority.NORMAL,
    EventType.JITSI_CONFERENCE_LEFT: EventPriority.NORMAL,
    EventType.JITSI_PARTICIPANT_JOINED: EventPriority.NORMAL,
    EventType.JITSI_PARTICIPANT_LEFT: EventPriority.NORMAL,
    EventType.JITSI_PARTICIPANT_MUTED: EventPriority.NORMAL,
    EventType.JITSI_PARTICIPANT_MENU_BUTTON_CLICK: EventPriority.NORMAL,
    EventType.JITSI_AUDIO_MUTE_STATUS_CHANGED: EventPriority.NORMAL,
    EventType.JITSI_VIDEO_MUTE_STATUS_CHANGED: EventPriority.NORMAL,
    EventType.JITSI_SPEAKER_DOMINANT_CHANGED: EventPriority.NORMAL,
    EventType.JITSI_DEVICE_LIST_CHANGED: EventPriority.NORMAL,
    EventType.JITSI_CAMERA_ERROR: EventPriority.NORMAL,
    EventType.JITSI_MIC_ERROR: EventPriority.NORMAL,
    EventType.JITSI_ERROR_OCCURRED: EventPriority.NORMAL,
    EventType.JITSI_PEER_CONNECTION_FAILURE: EventPriority.NORMAL,
    EventType.JITSI_SUSPEND_DETECTED: EventPriority.NORMAL,
    EventType.JITSI_TOOLBAR_BUTTON_CLICKED: EventPriority.NORMAL,
}

# Event type to schema version mapping
EVENT_SCHEMA_VERSIONS: dict[EventType, str] = {
    # All events start at v1
    EventType.BOOKING_CREATED: "v1",
    EventType.BOOKING_RESCHEDULED: "v1",
    EventType.BOOKING_REASSIGNED: "v1",
    EventType.BOOKING_CANCELLED: "v1",
    EventType.BOOKING_REMINDER_SENT: "v1",
    EventType.BOOKING_CLIENT_REASSIGNED: "v1",
    EventType.BOOKING_REJECTED: "v1",
    EventType.CHAT_CREATED: "v1",
    EventType.CHAT_DELETED: "v1",
    EventType.CHAT_MESSAGE_SENT: "v1",
    EventType.MEETING_URL_CREATED: "v1",
    EventType.MEETING_URL_DELETED: "v1",
    EventType.NOTIFICATION_EMAIL_SENT: "v1",
    EventType.NOTIFICATION_TELEGRAM_SENT: "v1",
    EventType.NOTIFICATION_SEND_REQUESTED: "v1",
    EventType.NOTIFICATION_PUSH_SENT: "v1",
    EventType.USER_EMAIL_CHANGE_REQUESTED: "v1",
    EventType.UNISENDER_STATUS_CREATED: "v1",
    EventType.GETSTREAM_CHANNEL_CREATED: "v1",
    EventType.GETSTREAM_CHANNEL_DELETED: "v1",
    EventType.GETSTREAM_MESSAGE_NEW: "v1",
    EventType.GETSTREAM_MESSAGE_UPDATED: "v1",
    EventType.GETSTREAM_MESSAGE_DELETED: "v1",
    EventType.GETSTREAM_MESSAGE_READ: "v1",
    EventType.JITSI_CONFERENCE_JOINED: "v1",
    EventType.JITSI_CONFERENCE_LEFT: "v1",
    EventType.JITSI_PARTICIPANT_JOINED: "v1",
    EventType.JITSI_PARTICIPANT_LEFT: "v1",
    EventType.JITSI_PARTICIPANT_MUTED: "v1",
    EventType.JITSI_PARTICIPANT_MENU_BUTTON_CLICK: "v1",
    EventType.JITSI_AUDIO_MUTE_STATUS_CHANGED: "v1",
    EventType.JITSI_VIDEO_MUTE_STATUS_CHANGED: "v1",
    EventType.JITSI_SPEAKER_DOMINANT_CHANGED: "v1",
    EventType.JITSI_DEVICE_LIST_CHANGED: "v1",
    EventType.JITSI_CAMERA_ERROR: "v1",
    EventType.JITSI_MIC_ERROR: "v1",
    EventType.JITSI_ERROR_OCCURRED: "v1",
    EventType.JITSI_PEER_CONNECTION_FAILURE: "v1",
    EventType.JITSI_SUSPEND_DETECTED: "v1",
    EventType.JITSI_TOOLBAR_BUTTON_CLICKED: "v1",
}
