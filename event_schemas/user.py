"""User management event payload schemas."""

from pydantic import BaseModel, EmailStr, Field

from event_schemas.types import UuidStr


class BookingClientReassignedPayload(BaseModel):
    """Payload for booking.client_reassigned event."""

    booking_uid: str = Field(..., description="Booking identifier")
    new_client_user_id: UuidStr = Field(..., description="UUID of the new client user")
    requested_by: str = Field(..., description="Admin email who requested the reassignment")

    model_config = {
        "json_schema_extra": {
            "example": {
                "booking_uid": "book-123",
                "new_client_user_id": "550e8400-e29b-41d4-a716-446655440001",
                "requested_by": "admin@company.com",
            }
        }
    }


class UserEmailChangeRequestedPayload(BaseModel):
    """Payload for user.email.change_requested event."""

    user_id: UuidStr = Field(..., description="UUID of the client user")
    old_email: EmailStr = Field(..., description="Current email before change")
    new_email: EmailStr = Field(..., description="New email to set")
    requested_by: str = Field(..., description="Admin email who requested the change")

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440001",
                "old_email": "old@example.com",
                "new_email": "new@example.com",
                "requested_by": "admin@company.com",
            }
        }
    }


class UserContactPayload(BaseModel):
    """A single contact channel for a synced user."""

    channel: str = Field(..., description="Contact channel, e.g. 'email' or 'telegram'")
    contact_id: str = Field(..., description="Channel-specific identifier")


class UserUpsertedPayload(BaseModel):
    """Payload for user.upserted — a cal.com row mapped to a user (source of truth: cal.com)."""

    email: EmailStr = Field(..., description="User email (unique within a role)")
    role: str = Field(..., description="'client' (cal.com Attendee) or 'organizer' (cal.com users)")
    time_zone: str | None = Field(None, description="IANA time zone from cal.com, or null")
    name: str | None = Field(None, description="Display name from cal.com, or null")
    contacts: list[UserContactPayload] = Field(default_factory=list, description="Extra contact channels")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "client@example.com",
                "role": "client",
                "time_zone": "Europe/Moscow",
                "name": "Jane Client",
                "contacts": [{"channel": "email", "contact_id": "client@example.com"}],
            }
        }
    }


class UserSyncedPayload(BaseModel):
    """Payload for user.synced — event-users announces the resolved user_id for a synced user."""

    email: EmailStr = Field(..., description="User email")
    role: str = Field(..., description="'client' or 'organizer'")
    user_id: UuidStr = Field(..., description="UUID assigned by event-users")
    time_zone: str | None = Field(None, description="IANA time zone, or null")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "client@example.com",
                "role": "client",
                "user_id": "550e8400-e29b-41d4-a716-446655440001",
                "time_zone": "Europe/Moscow",
            }
        }
    }
