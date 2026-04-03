"""Normalized payload structures using TypedDict.

Standard structure that event-receiver produces after normalization:
{
    "original": {...},      # Original payload (unchanged)
    "normalized": {         # Typed normalized structure
        "participants": [...],
        "booking": {...}
    }
}
"""

from typing import NotRequired, TypedDict


class NormalizedParticipant(TypedDict):
    """Normalized participant structure."""

    email: str
    role: NotRequired[str | None]
    time_zone: NotRequired[str | None]


class NormalizedBooking(TypedDict):
    """Normalized booking structure."""

    start_time: NotRequired[str | None]
    end_time: NotRequired[str | None]
    status: NotRequired[str | None]


class NormalizedData(TypedDict):
    """Core normalized structure with participants and booking."""

    participants: list[NormalizedParticipant]
    booking: NormalizedBooking


class NormalizedPayload(TypedDict):
    """Complete normalized payload structure.

    Contains both original payload and normalized standard structure.
    """

    original: dict
    normalized: NormalizedData
