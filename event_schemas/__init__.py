"""Shared event schemas for event-receiver and event-saver."""

from event_schemas.booking import (
    BookingCancelledPayload,
    BookingCreatedPayload,
    BookingReassignedPayload,
    BookingReminderSentPayload,
    BookingRescheduledPayload,
)
from event_schemas.chat import ChatCreatedPayload, ChatDeletedPayload, ChatMessageSentPayload
from event_schemas.external import (
    GetStreamEventPayload,
    JitsiEventPayload,
    UniSenderStatusPayload,
)
from event_schemas.meeting import MeetingUrlCreatedPayload, MeetingUrlDeletedPayload
from event_schemas.normalized import (
    NormalizedBooking,
    NormalizedData,
    NormalizedParticipant,
    NormalizedPayload,
)
from event_schemas.notification import (
    EmailNotificationPayload,
    EmailRejectionNotificationPayload,
    NotificationCommandPayload,
    NotificationRecipient,
    PushNotificationPayload,
    TelegramNotificationPayload,
)
from event_schemas.types import (
    EVENT_PRIORITIES,
    EVENT_SCHEMA_VERSIONS,
    ClientInfo,
    EventPriority,
    EventType,
    RecipientRole,
    SourceType,
    TriggerEvent,
    UserInfo,
)
from event_schemas.user import BookingClientReassignedPayload, UserEmailChangeRequestedPayload

__version__ = "0.1.0"

__all__ = [
    "EVENT_PRIORITIES",
    "EVENT_SCHEMA_VERSIONS",
    # Booking
    "BookingCancelledPayload",
    "BookingClientReassignedPayload",
    "BookingCreatedPayload",
    "BookingReassignedPayload",
    "BookingReminderSentPayload",
    "BookingRescheduledPayload",
    # Chat
    "ChatCreatedPayload",
    "ChatDeletedPayload",
    "ChatMessageSentPayload",
    "ClientInfo",
    # Notifications
    "EmailNotificationPayload",
    "EmailRejectionNotificationPayload",
    "EventPriority",
    # Types
    "EventType",
    "GetStreamEventPayload",
    "JitsiEventPayload",
    # Meeting
    "MeetingUrlCreatedPayload",
    "MeetingUrlDeletedPayload",
    "NormalizedBooking",
    "NormalizedData",
    "NormalizedParticipant",
    # Normalized structures
    "NormalizedPayload",
    "NotificationCommandPayload",
    "NotificationRecipient",
    "PushNotificationPayload",
    "RecipientRole",
    "SourceType",
    "TelegramNotificationPayload",
    "TriggerEvent",
    # External
    "UniSenderStatusPayload",
    "UserEmailChangeRequestedPayload",
    "UserInfo",
]
