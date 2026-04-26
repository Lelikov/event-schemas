"""User management event payload schemas."""

from pydantic import BaseModel, EmailStr, Field


class BookingClientReassignedPayload(BaseModel):
    """Payload for booking.client_reassigned event."""

    booking_uid: str = Field(..., description="Booking identifier")
    new_client_user_id: str = Field(..., description="UUID of the new client user")
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

    user_id: str = Field(..., description="UUID of the client user")
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
