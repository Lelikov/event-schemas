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
from event_schemas.notification import (
    EmailNotificationPayload,
    EmailRejectionNotificationPayload,
    TelegramNotificationPayload,
)
from event_schemas.normalized import (
    NormalizedBooking,
    NormalizedData,
    NormalizedParticipant,
    NormalizedPayload,
)
from event_schemas.types import (
    EVENT_PRIORITIES,
    EVENT_SCHEMA_VERSIONS,
    ClientInfo,
    EventPriority,
    EventType,
    RecipientRole,
    TriggerEvent,
    UserInfo,
)

__version__ = "0.1.0"

__all__ = [
    # Types
    "EventType",
    "EventPriority",
    "RecipientRole",
    "TriggerEvent",
    "UserInfo",
    "ClientInfo",
    "EVENT_PRIORITIES",
    "EVENT_SCHEMA_VERSIONS",
    # Normalized structures
    "NormalizedPayload",
    "NormalizedData",
    "NormalizedParticipant",
    "NormalizedBooking",
    # Booking
    "BookingCreatedPayload",
    "BookingRescheduledPayload",
    "BookingReassignedPayload",
    "BookingCancelledPayload",
    "BookingReminderSentPayload",
    # Chat
    "ChatCreatedPayload",
    "ChatDeletedPayload",
    "ChatMessageSentPayload",
    # Meeting
    "MeetingUrlCreatedPayload",
    "MeetingUrlDeletedPayload",
    # Notifications
    "EmailNotificationPayload",
    "EmailRejectionNotificationPayload",
    "TelegramNotificationPayload",
    # External
    "UniSenderStatusPayload",
    "GetStreamEventPayload",
    "JitsiEventPayload",
]
