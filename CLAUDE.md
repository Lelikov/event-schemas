# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Lint
ruff check .

# Type check
mypy event_schemas
```

No test suite exists — this is a schema library relying on strict typing for correctness.

## Architecture

This is a **shared Python package** providing type-safe event schemas consumed by event-receiver and event-saver services. All schemas are Pydantic v2 models.

### Module layout

- `types.py` — Core enums (`EventType`, `EventPriority`, `RecipientRole`, `TriggerEvent`) and base models (`UserInfo`, `ClientInfo`). Also contains `EVENT_PRIORITIES` (EventType → priority int) and `EVENT_SCHEMA_VERSIONS` (EventType → version string).
- `booking.py` — Payloads for booking lifecycle events (created, rescheduled, reassigned, cancelled, reminder sent).
- `chat.py` — Payloads for GetStream chat events (created, deleted, message sent).
- `meeting.py` — Payloads for Jitsi meeting URL events (created, deleted).
- `notification.py` — Payloads for email/Telegram notification events, including complex rejection payloads.
- `external.py` — Flexible payloads for third-party webhooks (UniSender, GetStream, Jitsi) that allow extra fields.
- `normalized.py` — `TypedDict`-based structures (`NormalizedPayload`, `NormalizedData`, `NormalizedParticipant`, `NormalizedBooking`) for downstream normalization; uses structural typing rather than runtime validation.
- `__init__.py` — Re-exports the full public API.

### Event priorities (used for RabbitMQ queue priority)

| Priority | Level | Examples |
|---|---|---|
| 10 | CRITICAL | Booking created/rescheduled/reassigned/cancelled |
| 7 | HIGH | Email/Telegram notifications, booking reminders |
| 5 | NORMAL | Chat, meetings, external integrations |
| 1 | LOW | (reserved) |

### Key conventions

- All event payloads inherit from Pydantic `BaseModel` with strict type annotations.
- Email fields use `EmailStr`; timezone fields use an IANA pattern validator.
- Schema versions live in `EVENT_SCHEMA_VERSIONS` and follow semver semantics (bump major for breaking changes).
- External webhook models (UniSender, GetStream, Jitsi) set `model_config = ConfigDict(extra="allow")` to handle variable upstream payloads.
- Python ≥ 3.14 is required; Ruff line length is 120.
