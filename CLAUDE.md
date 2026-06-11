# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv sync                # install with dev dependencies
uv run pytest          # run tests (envelope / queue specs / payload mapping)
uv run ruff check .    # lint
uv run mypy event_schemas  # type check
```

## Architecture

This is a **shared Python package** providing type-safe event schemas consumed by event-receiver and event-saver services. All schemas are Pydantic v2 models.

### Module layout

- `types.py` — Core enums (`EventType`, `EventPriority`, `RecipientRole`, `TriggerEvent`) and base models (`UserInfo`, `ClientInfo`). Also contains `EVENT_PRIORITIES` (EventType → priority int) and `EVENT_SCHEMA_VERSIONS` (EventType → version string).
- `queues.py` — **Single source of truth for the RabbitMQ topology**: `EVENTS_EXCHANGE`, `EVENTS_DLX`, `QueueSpec` (queue name + binding + canonical arguments), `ALL_QUEUES`, `SAVER_QUEUES`, `ROUTING_RULES`. One queue per consumer; fan-out via multiple queues on the same routing key.
- `envelope.py` — Canonical `{"original", "normalized"}` data envelope: `EventEnvelope`, `EnvelopeParticipant`, `unwrap_payload()`. Every RabbitMQ consumer MUST unwrap through this module.
- `attributes.py` — Canonical CloudEvent extension attribute names (`bookingid` / `ce-bookingid`, `traceid`, `spanid`, `idempotencykey`).
- `mapping.py` — `PAYLOAD_MODELS`: EventType → payload model for every event type.
- `booking.py` — Payloads for booking lifecycle events (created, rescheduled, reassigned, cancelled, reminder sent).
- `chat.py` — Payloads for GetStream chat events (created, deleted, message sent).
- `meeting.py` — Payloads for Jitsi meeting URL events (created, deleted).
- `notification.py` — Payloads for email/Telegram notification events, including complex rejection payloads.
- `external.py` — Flexible payloads for third-party webhooks (UniSender, GetStream, Jitsi) that allow extra fields.
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
- Email fields use `EmailStr`; timezone fields use `TimeZoneName` (validated against the zoneinfo IANA database); UUID-carrying id fields use `UuidStr` (str on the wire, UUID-format validated).
- Schema versions live in `EVENT_SCHEMA_VERSIONS` and follow semver semantics (bump major for breaking changes).
- External webhook models (UniSender, GetStream, Jitsi) set `model_config = ConfigDict(extra="allow")` to handle variable upstream payloads.
- Python ≥ 3.14 is required; Ruff line length is 120.

## Package Documentation

- `docs/SERVICE_OVERVIEW.md` — package structure, maturity, known issues
- `docs/API_CONTRACTS.md` — exported types, enums, and models
- `docs/DEPENDENCIES.md` — consumer services and failure modes
- `docs/AUDIT.md` — audit findings for this package

Cross-service architecture docs (message contracts, system topology, onboarding) are in `../docs/`.

<!-- code-review-graph MCP tools -->
## MCP Tools: code-review-graph

**IMPORTANT: This project has a knowledge graph. ALWAYS use the
code-review-graph MCP tools BEFORE using Grep/Glob/Read to explore
the codebase.** The graph is faster, cheaper (fewer tokens), and gives
you structural context (callers, dependents, test coverage) that file
scanning cannot.

### When to use graph tools FIRST

- **Exploring code**: `semantic_search_nodes` or `query_graph` instead of Grep
- **Understanding impact**: `get_impact_radius` instead of manually tracing imports
- **Code review**: `detect_changes` + `get_review_context` instead of reading entire files
- **Finding relationships**: `query_graph` with callers_of/callees_of/imports_of/tests_for
- **Architecture questions**: `get_architecture_overview` + `list_communities`

Fall back to Grep/Glob/Read **only** when the graph doesn't cover what you need.

### Key Tools

| Tool | Use when |
|------|----------|
| `detect_changes` | Reviewing code changes — gives risk-scored analysis |
| `get_review_context` | Need source snippets for review — token-efficient |
| `get_impact_radius` | Understanding blast radius of a change |
| `get_affected_flows` | Finding which execution paths are impacted |
| `query_graph` | Tracing callers, callees, imports, tests, dependencies |
| `semantic_search_nodes` | Finding functions/classes by name or keyword |
| `get_architecture_overview` | Understanding high-level codebase structure |
| `refactor_tool` | Planning renames, finding dead code |

### Workflow

1. The graph auto-updates on file changes (via hooks).
2. Use `detect_changes` for code review.
3. Use `get_affected_flows` to understand impact.
4. Use `query_graph` pattern="tests_for" to check coverage.
