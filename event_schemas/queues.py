"""Canonical RabbitMQ topology: exchanges, queues, bindings, and routing rules.

This module is the SINGLE source of truth for the broker topology.
Every service MUST declare queues using these specs (identical arguments),
otherwise RabbitMQ rejects the declaration with PRECONDITION_FAILED (406).

Topology rules:
- One topic exchange ``events`` for all inter-service messages.
- One topic dead-letter exchange ``events.dlx``.
- Each consumer service gets its OWN queue. Two services must never consume
  the same queue (round-robin splits the stream). Fan-out is achieved by
  binding several queues to the same routing key on the topic exchange.
- Every queue dead-letters to ``events.dlx`` with routing key ``<queue>.dlq``;
  a matching ``<queue>.dlq`` queue (24h TTL) is bound to the DLX.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

EVENTS_EXCHANGE = "events"
EVENTS_DLX = "events.dlx"
DLQ_SUFFIX = ".dlq"
DLQ_MESSAGE_TTL_MS = 86_400_000  # 24 hours
MAX_PRIORITY = 10


class RoutingKey(StrEnum):
    """Logical routing keys published to the ``events`` topic exchange."""

    BOOKING_LIFECYCLE = "events.booking.lifecycle"
    CHAT_LIFECYCLE = "events.chat.lifecycle"
    CHAT_ACTIVITY = "events.chat.activity"
    CHAT_EXTERNAL = "events.chat"
    MEETING_LIFECYCLE = "events.meeting.lifecycle"
    NOTIFICATION_COMMANDS = "events.notification.commands"
    NOTIFICATION_DELIVERY = "events.notification.delivery"
    JITSI = "events.jitsi"
    MAIL = "events.mail"
    USER_EMAIL = "events.user.email"
    USER_SYNCED = "events.user.synced"
    UNROUTED = "events.unrouted"


DEFAULT_ROUTING_KEY = RoutingKey.UNROUTED


@dataclass(frozen=True, slots=True)
class QueueSpec:
    """Canonical declaration of a single queue."""

    name: str
    binding: RoutingKey
    consumer: str  # service that owns/consumes this queue (documentation only)

    @property
    def dlq_name(self) -> str:
        return f"{self.name}{DLQ_SUFFIX}"

    @property
    def arguments(self) -> dict[str, Any]:
        """Arguments every declarer of this queue MUST use verbatim."""
        return {
            "x-max-priority": MAX_PRIORITY,
            "x-dead-letter-exchange": EVENTS_DLX,
            "x-dead-letter-routing-key": self.dlq_name,
        }

    @property
    def dlq_arguments(self) -> dict[str, Any]:
        return {"x-message-ttl": DLQ_MESSAGE_TTL_MS}


# --- Consumer queues (one queue per consumer service) ---

BOOKING_LIFECYCLE_SAVER_QUEUE = QueueSpec(
    name="events.booking.lifecycle.saver",
    binding=RoutingKey.BOOKING_LIFECYCLE,
    consumer="event-saver",
)
BOOKING_LIFECYCLE_BOOKING_QUEUE = QueueSpec(
    name="events.booking.lifecycle.booking",
    binding=RoutingKey.BOOKING_LIFECYCLE,
    consumer="event-booking",
)
CHAT_LIFECYCLE_QUEUE = QueueSpec(
    name="events.chat.lifecycle",
    binding=RoutingKey.CHAT_LIFECYCLE,
    consumer="event-saver",
)
CHAT_ACTIVITY_QUEUE = QueueSpec(
    name="events.chat.activity",
    binding=RoutingKey.CHAT_ACTIVITY,
    consumer="event-saver",
)
CHAT_EXTERNAL_QUEUE = QueueSpec(
    name="events.chat",
    binding=RoutingKey.CHAT_EXTERNAL,
    consumer="event-saver",
)
MEETING_LIFECYCLE_QUEUE = QueueSpec(
    name="events.meeting.lifecycle",
    binding=RoutingKey.MEETING_LIFECYCLE,
    consumer="event-saver",
)
NOTIFICATION_COMMANDS_QUEUE = QueueSpec(
    name="events.notification.commands",
    binding=RoutingKey.NOTIFICATION_COMMANDS,
    consumer="event-notifier",
)
NOTIFICATION_DELIVERY_QUEUE = QueueSpec(
    name="events.notification.delivery",
    binding=RoutingKey.NOTIFICATION_DELIVERY,
    consumer="event-saver",
)
JITSI_QUEUE = QueueSpec(
    name="events.jitsi",
    binding=RoutingKey.JITSI,
    consumer="event-saver",
)
MAIL_QUEUE = QueueSpec(
    name="events.mail",
    binding=RoutingKey.MAIL,
    consumer="event-saver",
)
USER_EMAIL_QUEUE = QueueSpec(
    name="events.user.email",
    binding=RoutingKey.USER_EMAIL,
    consumer="event-users",
)
USER_SYNCED_QUEUE = QueueSpec(
    name="events.user.synced",
    binding=RoutingKey.USER_SYNCED,
    consumer="event-saver",
)
UNROUTED_QUEUE = QueueSpec(
    name="events.unrouted",
    binding=RoutingKey.UNROUTED,
    consumer="event-saver",
)

ALL_QUEUES: tuple[QueueSpec, ...] = (
    BOOKING_LIFECYCLE_SAVER_QUEUE,
    BOOKING_LIFECYCLE_BOOKING_QUEUE,
    CHAT_LIFECYCLE_QUEUE,
    CHAT_ACTIVITY_QUEUE,
    CHAT_EXTERNAL_QUEUE,
    MEETING_LIFECYCLE_QUEUE,
    NOTIFICATION_COMMANDS_QUEUE,
    NOTIFICATION_DELIVERY_QUEUE,
    JITSI_QUEUE,
    MAIL_QUEUE,
    USER_EMAIL_QUEUE,
    USER_SYNCED_QUEUE,
    UNROUTED_QUEUE,
)

SAVER_QUEUES: tuple[QueueSpec, ...] = tuple(q for q in ALL_QUEUES if q.consumer == "event-saver")


@dataclass(frozen=True, slots=True)
class RoutingRuleSpec:
    """Glob rule mapping (source, type) of a CloudEvent to a routing key."""

    destination: RoutingKey
    source_pattern: str = "*"
    type_pattern: str = "*"


ROUTING_RULES: tuple[RoutingRuleSpec, ...] = (
    # Booking lifecycle (incl. reminder_sent: persisted as part of booking history)
    RoutingRuleSpec(RoutingKey.BOOKING_LIFECYCLE, "booking", "booking.created"),
    RoutingRuleSpec(RoutingKey.BOOKING_LIFECYCLE, "booking", "booking.rescheduled"),
    RoutingRuleSpec(RoutingKey.BOOKING_LIFECYCLE, "booking", "booking.reassigned"),
    RoutingRuleSpec(RoutingKey.BOOKING_LIFECYCLE, "booking", "booking.cancelled"),
    RoutingRuleSpec(RoutingKey.BOOKING_LIFECYCLE, "booking", "booking.rejected"),
    RoutingRuleSpec(RoutingKey.BOOKING_LIFECYCLE, "booking", "booking.reminder_sent"),
    RoutingRuleSpec(RoutingKey.BOOKING_LIFECYCLE, "admin", "booking.client_reassigned"),
    # Chat lifecycle/activity produced by event-booking
    RoutingRuleSpec(RoutingKey.CHAT_LIFECYCLE, "booking", "chat.created"),
    RoutingRuleSpec(RoutingKey.CHAT_LIFECYCLE, "booking", "chat.deleted"),
    RoutingRuleSpec(RoutingKey.CHAT_ACTIVITY, "booking", "chat.message_sent"),
    # Meeting URLs
    RoutingRuleSpec(RoutingKey.MEETING_LIFECYCLE, "booking", "meeting.url_created"),
    RoutingRuleSpec(RoutingKey.MEETING_LIFECYCLE, "booking", "meeting.url_deleted"),
    # Notification commands and delivery results
    RoutingRuleSpec(RoutingKey.NOTIFICATION_COMMANDS, "*", "notification.send_requested"),
    RoutingRuleSpec(RoutingKey.NOTIFICATION_DELIVERY, "*", "notification.email.message_sent"),
    RoutingRuleSpec(RoutingKey.NOTIFICATION_DELIVERY, "*", "notification.telegram.message_sent"),
    RoutingRuleSpec(RoutingKey.NOTIFICATION_DELIVERY, "*", "notification.push.message_sent"),
    # External integrations
    RoutingRuleSpec(RoutingKey.JITSI, "jitsi*", "*"),
    RoutingRuleSpec(RoutingKey.MAIL, "unisender-go", "unisender.*"),
    RoutingRuleSpec(RoutingKey.CHAT_EXTERNAL, "getstream", "getstream.*"),
    # Admin-originated user management
    RoutingRuleSpec(RoutingKey.USER_EMAIL, "admin", "user.email.*"),
    RoutingRuleSpec(RoutingKey.USER_EMAIL, "db-sync", "user.upserted"),
    RoutingRuleSpec(RoutingKey.USER_SYNCED, "event-users", "user.synced"),
)
