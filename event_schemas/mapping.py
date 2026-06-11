"""Canonical EventType -> payload model mapping.

``PAYLOAD_MODELS[event_type]`` is the pydantic model describing the
``original`` section of the envelope (see :mod:`event_schemas.envelope`)
for that event type. Producers validate before publishing; consumers parse
with ``EventEnvelope.parse_payload(PAYLOAD_MODELS[event_type])``.

External pass-through types (jitsi.*, getstream.*, unisender.*) map to
lenient ``extra="allow"`` models. Event types absent from this mapping have
no defined payload contract (consumers must treat ``original`` as opaque).
"""

from pydantic import BaseModel

from event_schemas.booking import (
    BookingCancelledPayload,
    BookingCreatedPayload,
    BookingReassignedPayload,
    BookingRejectedPayload,
    BookingReminderSentPayload,
    BookingRescheduledPayload,
)
from event_schemas.chat import ChatCreatedPayload, ChatDeletedPayload, ChatMessageSentPayload
from event_schemas.external import GetStreamEventPayload, JitsiEventPayload, UniSenderStatusPayload
from event_schemas.meeting import MeetingUrlCreatedPayload, MeetingUrlDeletedPayload
from event_schemas.notification import (
    EmailNotificationPayload,
    NotificationCommandPayload,
    PushNotificationPayload,
    TelegramNotificationPayload,
)
from event_schemas.types import EventType
from event_schemas.user import BookingClientReassignedPayload, UserEmailChangeRequestedPayload

PAYLOAD_MODELS: dict[EventType, type[BaseModel]] = {
    # Booking lifecycle
    EventType.BOOKING_CREATED: BookingCreatedPayload,
    EventType.BOOKING_RESCHEDULED: BookingRescheduledPayload,
    EventType.BOOKING_REASSIGNED: BookingReassignedPayload,
    EventType.BOOKING_CANCELLED: BookingCancelledPayload,
    EventType.BOOKING_REJECTED: BookingRejectedPayload,
    EventType.BOOKING_REMINDER_SENT: BookingReminderSentPayload,
    EventType.BOOKING_CLIENT_REASSIGNED: BookingClientReassignedPayload,
    # Chat
    EventType.CHAT_CREATED: ChatCreatedPayload,
    EventType.CHAT_DELETED: ChatDeletedPayload,
    EventType.CHAT_MESSAGE_SENT: ChatMessageSentPayload,
    # Meeting
    EventType.MEETING_URL_CREATED: MeetingUrlCreatedPayload,
    EventType.MEETING_URL_DELETED: MeetingUrlDeletedPayload,
    # Notifications
    EventType.NOTIFICATION_SEND_REQUESTED: NotificationCommandPayload,
    EventType.NOTIFICATION_EMAIL_SENT: EmailNotificationPayload,
    EventType.NOTIFICATION_TELEGRAM_SENT: TelegramNotificationPayload,
    EventType.NOTIFICATION_PUSH_SENT: PushNotificationPayload,
    # User management
    EventType.USER_EMAIL_CHANGE_REQUESTED: UserEmailChangeRequestedPayload,
    # External pass-through
    EventType.UNISENDER_STATUS_CREATED: UniSenderStatusPayload,
}

_GETSTREAM_TYPES = (t for t in EventType if t.value.startswith("getstream."))
_JITSI_TYPES = (t for t in EventType if t.value.startswith("jitsi."))

PAYLOAD_MODELS.update(dict.fromkeys(_GETSTREAM_TYPES, GetStreamEventPayload))
PAYLOAD_MODELS.update(dict.fromkeys(_JITSI_TYPES, JitsiEventPayload))
