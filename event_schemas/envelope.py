"""Canonical CloudEvent data envelope.

event-receiver wraps EVERY published payload as::

    {
        "original": {...},      # domain payload, exactly as produced
        "normalized": {
            "participants": [{"email", "role", "time_zone", "locale", "user_id"}, ...]
        }
    }

``original`` is what consumers parse with the payload models from
:mod:`event_schemas` (see ``PAYLOAD_MODELS``). ``normalized.participants``
is the receiver-enriched participant list (user_id resolved via event-users).

Consumers MUST go through :class:`EventEnvelope` / :func:`unwrap_payload`
instead of reading top-level keys of CloudEvent data.
"""

from typing import Any, TypeVar

from pydantic import BaseModel, Field

ModelT = TypeVar("ModelT", bound=BaseModel)


class EnvelopeParticipant(BaseModel):
    """Receiver-enriched participant inside ``normalized.participants``."""

    email: str
    role: str | None = None
    time_zone: str | None = None
    locale: str | None = None  # BCP-47-ish language tag from the producer (e.g. "ru", "en"); None = unknown
    user_id: str | None = None

    model_config = {"extra": "allow"}


class NormalizedSection(BaseModel):
    """The ``normalized`` section of the envelope."""

    participants: list[EnvelopeParticipant] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class EventEnvelope(BaseModel):
    """Typed accessor for the canonical ``{"original", "normalized"}`` envelope."""

    original: dict[str, Any] = Field(default_factory=dict)
    normalized: NormalizedSection = Field(default_factory=NormalizedSection)

    model_config = {"extra": "allow"}

    def parse_payload(self, model: type[ModelT]) -> ModelT:
        """Validate ``original`` against a canonical payload model."""
        return model.model_validate(self.original)


def unwrap_payload(data: dict[str, Any] | None) -> dict[str, Any]:
    """Return the domain payload from CloudEvent data.

    Tolerates both enveloped (``{"original": ...}``) and bare payloads, so
    consumers never silently read envelope keys as domain fields.
    """
    if not data:
        return {}
    original = data.get("original")
    if isinstance(original, dict):
        return original
    return data
