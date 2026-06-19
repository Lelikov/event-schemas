import pytest
from pydantic import ValidationError

from event_schemas.user import UserContactPayload, UserSyncedPayload, UserUpsertedPayload


def test_user_upserted_minimal() -> None:
    p = UserUpsertedPayload(email="a@b.c", role="client", time_zone=None, name=None)
    assert p.email == "a@b.c"
    assert p.contacts == []


def test_user_upserted_with_contacts() -> None:
    p = UserUpsertedPayload(
        email="a@b.c",
        role="organizer",
        time_zone="Europe/Moscow",
        name="Org",
        contacts=[UserContactPayload(channel="email", contact_id="a@b.c")],
    )
    assert p.contacts[0].channel == "email"


def test_user_synced_requires_uuid() -> None:
    ok = UserSyncedPayload(email="a@b.c", role="client", user_id="550e8400-e29b-41d4-a716-446655440001", time_zone=None)
    assert ok.role == "client"
    with pytest.raises(ValidationError):
        UserSyncedPayload(email="a@b.c", role="client", user_id="not-a-uuid", time_zone=None)
