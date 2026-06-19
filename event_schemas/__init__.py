"""Shared event schemas, broker topology and envelope contracts for all event services."""

from event_schemas.attributes import (
    BOOKING_ID_ATTRIBUTE,
    BOOKING_ID_HEADER,
    CE_HEADER_PREFIX,
    IDEMPOTENCY_KEY_ATTRIBUTE,
    IDEMPOTENCY_KEY_HEADER,
    SPAN_ID_ATTRIBUTE,
    SPAN_ID_HEADER,
    TRACE_ID_ATTRIBUTE,
    TRACE_ID_HEADER,
)
from event_schemas.booking import (
    BookingCancelledPayload,
    BookingCreatedPayload,
    BookingParticipant,
    BookingReassignedPayload,
    BookingRejectedPayload,
    BookingReminderSentPayload,
    BookingRescheduledPayload,
)
from event_schemas.chat import ChatCreatedPayload, ChatDeletedPayload, ChatMessageSentPayload
from event_schemas.envelope import (
    EnvelopeParticipant,
    EventEnvelope,
    NormalizedSection,
    unwrap_payload,
)
from event_schemas.external import (
    GetStreamEventPayload,
    JitsiEventPayload,
    UniSenderStatusPayload,
)
from event_schemas.mapping import PAYLOAD_MODELS
from event_schemas.meeting import MeetingUrlCreatedPayload, MeetingUrlDeletedPayload
from event_schemas.notification import (
    EmailNotificationPayload,
    NotificationCommandPayload,
    NotificationRecipient,
    PushNotificationPayload,
    TelegramNotificationPayload,
)
from event_schemas.queues import (
    ALL_QUEUES,
    DEFAULT_ROUTING_KEY,
    DLQ_MESSAGE_TTL_MS,
    DLQ_SUFFIX,
    EVENTS_DLX,
    EVENTS_EXCHANGE,
    MAX_PRIORITY,
    ROUTING_RULES,
    SAVER_QUEUES,
    USER_SYNCED_QUEUE,
    QueueSpec,
    RoutingKey,
    RoutingRuleSpec,
)
from event_schemas.types import (
    EVENT_PRIORITIES,
    EVENT_SCHEMA_VERSIONS,
    ClientInfo,
    EventPriority,
    EventType,
    RecipientRole,
    SourceType,
    TimeZoneName,
    TriggerEvent,
    UserInfo,
    UuidStr,
)
from event_schemas.user import (
    BookingClientReassignedPayload,
    UserContactPayload,
    UserEmailChangeRequestedPayload,
    UserSyncedPayload,
    UserUpsertedPayload,
)

__version__ = "0.5.0"

__all__ = [
    "ALL_QUEUES",
    "BOOKING_ID_ATTRIBUTE",
    "BOOKING_ID_HEADER",
    "CE_HEADER_PREFIX",
    "DEFAULT_ROUTING_KEY",
    "DLQ_MESSAGE_TTL_MS",
    "DLQ_SUFFIX",
    "EVENTS_DLX",
    "EVENTS_EXCHANGE",
    "EVENT_PRIORITIES",
    "EVENT_SCHEMA_VERSIONS",
    "IDEMPOTENCY_KEY_ATTRIBUTE",
    "IDEMPOTENCY_KEY_HEADER",
    "MAX_PRIORITY",
    "PAYLOAD_MODELS",
    "ROUTING_RULES",
    "SAVER_QUEUES",
    "SPAN_ID_ATTRIBUTE",
    "SPAN_ID_HEADER",
    "TRACE_ID_ATTRIBUTE",
    "TRACE_ID_HEADER",
    "USER_SYNCED_QUEUE",
    # Booking
    "BookingCancelledPayload",
    "BookingClientReassignedPayload",
    "BookingCreatedPayload",
    "BookingParticipant",
    "BookingReassignedPayload",
    "BookingRejectedPayload",
    "BookingReminderSentPayload",
    "BookingRescheduledPayload",
    # Chat
    "ChatCreatedPayload",
    "ChatDeletedPayload",
    "ChatMessageSentPayload",
    "ClientInfo",
    # Notifications
    "EmailNotificationPayload",
    # Envelope
    "EnvelopeParticipant",
    "EventEnvelope",
    "EventPriority",
    # Types
    "EventType",
    "GetStreamEventPayload",
    "JitsiEventPayload",
    # Meeting
    "MeetingUrlCreatedPayload",
    "MeetingUrlDeletedPayload",
    "NormalizedSection",
    "NotificationCommandPayload",
    "NotificationRecipient",
    "PushNotificationPayload",
    # Queues / topology
    "QueueSpec",
    "RecipientRole",
    "RoutingKey",
    "RoutingRuleSpec",
    "SourceType",
    "TelegramNotificationPayload",
    "TimeZoneName",
    "TriggerEvent",
    # External
    "UniSenderStatusPayload",
    "UserContactPayload",
    "UserEmailChangeRequestedPayload",
    "UserInfo",
    "UserSyncedPayload",
    "UserUpsertedPayload",
    "UuidStr",
    "unwrap_payload",
]
