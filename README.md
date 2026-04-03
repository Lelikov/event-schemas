# event-schemas

Shared event schemas for event-receiver and event-saver services.

## Purpose

This package provides:
- **EventType enum**: Type-safe event type constants
- **Pydantic models**: Validated schemas for all event payloads
- **Shared types**: Common data structures (UserInfo, ClientInfo, etc.)
- **Event metadata**: Priority, versioning support

## Installation

```bash
# From GitHub (latest)
pip install git+https://github.com/Lelikov/event-schemas.git

# From GitHub (specific tag)
pip install git+https://github.com/Lelikov/event-schemas.git@v0.1.0

# From GitHub (specific branch)
pip install git+https://github.com/Lelikov/event-schemas.git@main

# Local development
pip install -e /path/to/event-schemas

# From private PyPI (if published)
pip install event-schemas
```

### Adding to Dependencies

**requirements.txt:**
```
event-schemas @ git+https://github.com/Lelikov/event-schemas.git@v0.1.0
```

**pyproject.toml:**
```toml
[project]
dependencies = [
    "event-schemas @ git+https://github.com/Lelikov/event-schemas.git@v0.1.0"
]
```

## Usage

### EventType Enum

```python
from event_schemas.types import EventType

# Type-safe event types
event_type = EventType.BOOKING_CREATED
```

### Payload Validation

```python
from event_schemas.booking import BookingCreatedPayload

# Validate incoming data
payload = BookingCreatedPayload(
    user={"email": "organizer@example.com", "time_zone": "UTC"},
    client={"email": "client@example.com", "time_zone": "UTC"},
    start_time="2024-03-01T10:00:00Z",
    end_time="2024-03-01T11:00:00Z",
)

# Serialize to dict
data = payload.model_dump()
```

### Event Priority

```python
from event_schemas.types import EventPriority, EVENT_PRIORITIES

priority = EVENT_PRIORITIES.get(EventType.BOOKING_CANCELLED)
# Returns: EventPriority.CRITICAL (10)
```

## Package Structure

```
event_schemas/
├── __init__.py          # Public API
├── types.py             # EventType enum, EventPriority, shared types
├── booking.py           # Booking event schemas
├── chat.py              # Chat event schemas
├── notification.py      # Notification event schemas
├── meeting.py           # Meeting event schemas
└── external.py          # External integration events (UniSender, GetStream, Jitsi)
```

## Adding New Events

1. Add event type to `EventType` enum in `types.py`
2. Create Pydantic model in appropriate file
3. Add priority to `EVENT_PRIORITIES` mapping
4. Update version in `pyproject.toml`
5. Tag release with semver

## Versioning

This package follows [Semantic Versioning](https://semver.org/):
- **Major**: Breaking changes to event schemas
- **Minor**: New event types or backwards-compatible additions
- **Patch**: Bug fixes, documentation updates

## Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run linter
ruff check .

# Run type checker
mypy event_schemas
```
