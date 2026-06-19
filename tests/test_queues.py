"""Tests for the canonical RabbitMQ topology specs."""

from event_schemas.queues import (
    ALL_QUEUES,
    BOOKING_LIFECYCLE_BOOKING_QUEUE,
    BOOKING_LIFECYCLE_SAVER_QUEUE,
    EVENTS_DLX,
    ROUTING_RULES,
    SAVER_QUEUES,
    USER_SYNCED_QUEUE,
    RoutingKey,
)


def test_queue_names_are_unique() -> None:
    names = [q.name for q in ALL_QUEUES]

    assert len(names) == len(set(names))


def test_no_two_services_consume_the_same_queue() -> None:
    by_name: dict[str, str] = {}
    for queue in ALL_QUEUES:
        assert queue.name not in by_name
        by_name[queue.name] = queue.consumer


def test_booking_lifecycle_fanout_via_separate_queues_same_binding() -> None:
    assert BOOKING_LIFECYCLE_SAVER_QUEUE.name != BOOKING_LIFECYCLE_BOOKING_QUEUE.name
    assert BOOKING_LIFECYCLE_SAVER_QUEUE.binding == RoutingKey.BOOKING_LIFECYCLE
    assert BOOKING_LIFECYCLE_BOOKING_QUEUE.binding == RoutingKey.BOOKING_LIFECYCLE
    assert BOOKING_LIFECYCLE_SAVER_QUEUE.consumer == "event-saver"
    assert BOOKING_LIFECYCLE_BOOKING_QUEUE.consumer == "event-booking"


def test_canonical_queue_arguments() -> None:
    for queue in ALL_QUEUES:
        assert queue.arguments == {
            "x-max-priority": 10,
            "x-dead-letter-exchange": EVENTS_DLX,
            "x-dead-letter-routing-key": f"{queue.name}.dlq",
        }
        assert queue.dlq_name == f"{queue.name}.dlq"
        assert queue.dlq_arguments == {"x-message-ttl": 86_400_000}


def test_every_routing_rule_destination_has_a_bound_queue() -> None:
    bound_keys = {q.binding for q in ALL_QUEUES}

    for rule in ROUTING_RULES:
        assert rule.destination in bound_keys, rule


def test_booking_reminder_queue_removed() -> None:
    assert all(q.name != "events.booking.reminder" for q in ALL_QUEUES)

    reminder_rules = [r for r in ROUTING_RULES if r.type_pattern == "booking.reminder_sent"]
    assert len(reminder_rules) == 1
    assert reminder_rules[0].destination == RoutingKey.BOOKING_LIFECYCLE


def test_saver_queues_subset() -> None:
    assert set(SAVER_QUEUES) == {q for q in ALL_QUEUES if q.consumer == "event-saver"}
    assert BOOKING_LIFECYCLE_SAVER_QUEUE in SAVER_QUEUES
    assert BOOKING_LIFECYCLE_BOOKING_QUEUE not in SAVER_QUEUES


def test_user_synced_queue_is_saver_owned() -> None:
    assert USER_SYNCED_QUEUE.name == "events.user.synced"
    assert USER_SYNCED_QUEUE.binding == RoutingKey.USER_SYNCED
    assert USER_SYNCED_QUEUE in ALL_QUEUES
    assert USER_SYNCED_QUEUE in SAVER_QUEUES  # consumer == "event-saver"


def test_sync_routing_rules_exist() -> None:
    rules = {(r.source_pattern, r.type_pattern): r.destination for r in ROUTING_RULES}
    assert rules[("db-sync", "user.upserted")] == RoutingKey.USER_EMAIL
    assert rules[("event-users", "user.synced")] == RoutingKey.USER_SYNCED
