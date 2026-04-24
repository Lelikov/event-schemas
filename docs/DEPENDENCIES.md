# event-schemas: Dependencies

## Runtime Dependencies

**Single dependency:** `pydantic[email]>=2.0` (`pyproject.toml:11`)

No other runtime dependencies. The library is pure Python with Pydantic models only.

## Dev Dependencies

- `ruff>=0.8.0` -- linting/formatting
- `mypy>=1.0` -- static type checking
- `code-review-graph>=2.3.1` -- knowledge graph tooling

**Source:** `pyproject.toml:14-16, 38-40`

---

## Required By

### event-receiver (active dependency)

event-receiver imports event-schemas at runtime in three locations:

| File | Imports |
|------|---------|
| `event_receiver/adapters/publisher.py:5` | `EVENT_PRIORITIES`, `EVENT_SCHEMA_VERSIONS`, `EventPriority`, `EventType` |
| `event_receiver/controllers/ingest.py:9-10` | `BookingCreatedPayload`, `EventType` |
| `event_receiver/normalizers.py:10-18` | `BookingReassignedPayload`, `GetStreamEventPayload`, `JitsiEventPayload`, `UniSenderStatusPayload`, `NormalizedParticipant`, `NormalizedData`, `NormalizedPayload`, `EventType` |

### event-saver (no runtime import)

Despite being the primary consumer of events produced by event-receiver, **event-saver does not import event-schemas in any runtime `.py` file**. It has its own parallel type system. Integration proposals exist in `event-saver/docs/` but remain unimplemented.

---

## Impact of Updating event-schemas Without Updating Consumers

| Change type | Impact on event-receiver | Impact on event-saver |
|-------------|--------------------------|----------------------|
| Add new field to a payload model | None (additive) | None (no import) |
| Remove or rename a field | **Breaking** -- ingest/normalizer will fail at import or validation time | None (no import) |
| Change `EventType` enum member name | **Breaking** -- references in publisher, ingest, normalizer break | None (no import) |
| Change `EventType` enum value (string) | **Breaking** -- routing keys change, messages may go to wrong queues | None directly, but event-saver routes on string patterns so behavior may change |
| Add new `EventType` member | Safe, but without corresponding normalizer logic the event passes through unnormalized | None |
| Bump `EVENT_SCHEMA_VERSIONS` value | No runtime effect (version is cosmetic) | No effect |
| Change `EVENT_PRIORITIES` value | Changes RabbitMQ message priority for that event type | None |

**Key risk:** Because event-saver does not depend on this library, there is no mechanism to detect schema drift between the shared definitions and event-saver's actual processing logic.

---

## Known Drift: event-saver's Divergent EventType Enum

**Source:** `event-saver/event_saver/event_types.py:20-37` vs `event-schemas/event_schemas/types.py:8-43`

event-saver defines its own `EventType` enum with entirely different string values:

| Concept | event-schemas value | event-saver value |
|---------|--------------------|--------------------|
| Booking created | `"booking.created"` | `"booking.events.v1.booking.created.create"` |
| Booking cancelled | `"booking.cancelled"` | `"booking.events.v1.booking.cancelled.create"` |
| Booking reassigned | `"booking.reassigned"` | `"booking.events.v1.booking.reassigned.create"` |
| GetStream channel created | `"getstream.channel.created"` | `"getstream.events.v1.channel.created.create"` |
| GetStream message new | `"getstream.message.new"` | `"getstream.events.v1.message.new.create"` |
| UniSender status | `"unisender.events.v1.transactional.status.create"` | `"unisender.events.v1.transactional.status.create"` (only match) |

**Consequences:**

1. The shared library's `EventType` enum is irrelevant to event-saver -- the two services use different string identifiers for the same logical events.
2. Adding/changing members in event-schemas has zero effect on event-saver behavior.
3. There is no compile-time or CI check that detects drift between the two enums.
4. The only string value that matches between both enums is `UNISENDER_STATUS_CREATED`.

**Additional drift:** event-saver is missing `BOOKING_RESCHEDULED` from its enum entirely (audit finding MEDIUM-4), though it routes the event by pattern match.

---

## Architectural Recommendation

The dual-enum situation means event-schemas fails at its primary goal of being a "single source of truth." Until event-saver adopts the shared library (or the shared library adopts event-saver's URN format), schema changes must be coordinated manually across both codebases with no automated safety net.
