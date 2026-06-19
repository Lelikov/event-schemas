from event_schemas.types import EVENT_PRIORITIES, EVENT_SCHEMA_VERSIONS, EventPriority, EventType


def test_user_upserted_and_synced_are_critical() -> None:
    assert EVENT_PRIORITIES[EventType.USER_UPSERTED] == EventPriority.CRITICAL
    assert EVENT_PRIORITIES[EventType.USER_SYNCED] == EventPriority.CRITICAL


def test_user_upserted_and_synced_have_schema_versions() -> None:
    assert EVENT_SCHEMA_VERSIONS[EventType.USER_UPSERTED] == "v1"
    assert EVENT_SCHEMA_VERSIONS[EventType.USER_SYNCED] == "v1"
