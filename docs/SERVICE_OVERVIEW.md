# event-schemas: Service Overview

## Role

`event-schemas` is a **shared Python library** (not a runtime service). It provides Pydantic v2 models, enums, and constants that define the canonical shape of all CloudEvents flowing through the system. It is installed as a local pip package by consumer services.

**Source:** `event-schemas/pyproject.toml:1-4`

---

## Consumer Services

### event-receiver (active consumer)

Imports at runtime:
- `EventType`, `EVENT_PRIORITIES`, `EVENT_SCHEMA_VERSIONS`, `EventPriority` -- used by the RabbitMQ publisher to set message priority and `dataschema` CloudEvent attribute (`event-receiver/event_receiver/adapters/publisher.py:5`)
- `BookingCreatedPayload` -- validated in the ingest controller (`event-receiver/event_receiver/controllers/ingest.py:9`)
- `BookingReassignedPayload`, `GetStreamEventPayload`, `JitsiEventPayload`, `UniSenderStatusPayload`, `NormalizedParticipant`, `NormalizedData`, `NormalizedPayload` -- used in normalizers (`event-receiver/event_receiver/normalizers.py:10-18`)

### event-saver (does NOT import at runtime)

Despite being the largest downstream consumer of events, event-saver **does not import event-schemas in any runtime `.py` file**. It maintains its own divergent `EventType` enum at `event-saver/event_saver/event_types.py`. Integration proposals exist in `event-saver/docs/` but have not been implemented.

---

## Module Layout

| Module | Purpose | Key exports |
|--------|---------|-------------|
| `types.py` | Core enums and base models | `SourceType`, `EventType`, `EventPriority`, `RecipientRole`, `TriggerEvent`, `UserInfo`, `ClientInfo`, `EVENT_PRIORITIES`, `EVENT_SCHEMA_VERSIONS` |
| `booking.py` | Booking lifecycle payloads | `BookingCreatedPayload`, `BookingRescheduledPayload`, `BookingReassignedPayload`, `BookingCancelledPayload`, `BookingReminderSentPayload` |
| `chat.py` | GetStream chat payloads | `ChatCreatedPayload`, `ChatDeletedPayload`, `ChatMessageSentPayload` |
| `meeting.py` | Jitsi meeting URL payloads | `MeetingUrlCreatedPayload`, `MeetingUrlDeletedPayload` |
| `notification.py` | Notification delivery payloads | `EmailNotificationPayload`, `EmailRejectionNotificationPayload`, `TelegramNotificationPayload`, `NotificationCommandPayload`, `PushNotificationPayload`, `NotificationRecipient` |
| `external.py` | Third-party webhook payloads (flexible) | `UniSenderStatusPayload`, `GetStreamEventPayload`, `JitsiEventPayload` |
| `normalized.py` | TypedDict structures for normalized output | `NormalizedPayload`, `NormalizedData`, `NormalizedParticipant`, `NormalizedBooking` |
| `__init__.py` | Public API re-exports | All of the above via `__all__` |

**Source:** `event-schemas/event_schemas/__init__.py:1-83`

---

## Priority System

Four priority levels control RabbitMQ message ordering (`types.py:46-52`):

| Level | Value | Event types |
|-------|-------|-------------|
| CRITICAL | 10 | `booking.created`, `booking.rescheduled`, `booking.reassigned`, `booking.cancelled` |
| HIGH | 7 | `notification.email.message_sent`, `notification.telegram.message_sent`, `notification.send_requested`, `notification.push.message_sent`, `booking.reminder_sent` |
| NORMAL | 5 | All chat events, meeting events, and external integrations (GetStream, Jitsi, UniSender) |
| LOW | 1 | Reserved -- no events currently assigned |

Complete mapping: `types.py` (35 entries covering all `EventType` members).

---

## Versioning

### Package Version

Current: `0.1.5` (`pyproject.toml:3`). No changelog or release process is documented.

### Schema Versions (`EVENT_SCHEMA_VERSIONS`)

`types.py:119-145` maps every `EventType` to a semver string. All values are currently `"v1"`.

Intended semantics (per `CLAUDE.md`):
- Bump major for breaking changes to a payload schema
- Bump minor for additive changes

**Reality:** Versioning is cosmetic. The version string is embedded in the `dataschema` CloudEvent URI by event-receiver's publisher but **no consumer checks or enforces it** (audit finding MEDIUM-2).

---

## Known Limitations

1. **Versioning not enforced** -- `EVENT_SCHEMA_VERSIONS` populates a CloudEvent attribute that no consumer reads. Version bumps have no effect on routing or validation.

2. **Dual EventType enums** -- `event-saver` maintains its own `EventType` at `event-saver/event_saver/event_types.py:20-37` with entirely different string values (e.g., `"booking.events.v1.booking.created.create"` vs `"booking.created"`). The shared library is therefore not shared with the largest consumer (audit finding CRITICAL-1).

3. **No test suite** -- Library relies on strict typing for correctness. However, map completeness, field existence, and enum spelling are not verified programmatically (audit finding LOW-1).

4. **No EventType-to-model mapping** -- There is no programmatic way to look up which Pydantic model corresponds to a given EventType, leading to ad-hoc `match` dispatch in consumers (audit finding HIGH-1).

5. **`EmailRejectionNotificationPayload` is orphaned** -- Defined in `notification.py:31-62` and exported, but not wired to any `EventType` enum member and not used by any consumer.
