# event-schemas Audit Findings

Audited: 2026-04-20. Updated: 2026-06-11 (audit-v2 fixes on branch `audit-fixes`).

---

## CRITICAL

### [CRITICAL-1] event-saver defines its own EventType enum with incompatible string values

Services affected: event-schemas, event-saver
Location: `event-schemas/event_schemas/types.py:8-43`, `event-saver/event_saver/event_types.py:20-37`
Description: `event-schemas` defines `EventType.BOOKING_CREATED = "booking.created"` while `event-saver` defines its own `EventType.BOOKING_CREATED = "booking.events.v1.booking.created.create"`. The two enums share the same class name but have entirely different string values for every member. This means event-saver does **not** use the shared `event-schemas` EventType at all -- it has a parallel, divergent enum. The "shared schema library" is therefore not shared with the largest consumer. Any field name or payload structure change in `event-schemas` will not be noticed by event-saver at build time.
Recommendation: Decide on a single canonical EventType enum in `event-schemas`. If event-saver needs the `*.events.v1.*.create` URN format, either make that the canonical form or add a mapping/alias layer. Remove the duplicate enum from event-saver.

---

### [CRITICAL-2] ~~UserInfo missing `time_zone` field referenced at runtime by event-receiver normalizer~~ — RESOLVED

Services affected: event-schemas, event-receiver
Location: `event-schemas/event_schemas/types.py`
Resolution: `UserInfo` now declares `time_zone: str | None = None`. The `AttributeError` that previously caused every `booking.reassigned` normalization to silently fail is eliminated.

---

### [CRITICAL-3] Invalid multi-exception `except` syntax in normalizers.py (Python syntax error)

Services affected: event-receiver
Location: `event-receiver/event_receiver/normalizers.py:47`, `event-receiver/event_receiver/normalizers.py:151`
Description: Lines 47 and 151 use `except ValidationError, KeyError, ValueError:` and `except ValueError, UnicodeDecodeError, binascii.Error:` respectively. In Python 3, this syntax is invalid -- multiple exception types must be parenthesized: `except (ValidationError, KeyError, ValueError):`. Without parentheses, Python 3 interprets the second name as the binding variable, so only the first exception type is actually caught. This means `KeyError` and `ValueError` on line 47, and `UnicodeDecodeError`/`binascii.Error` on line 151, are **not caught**, and will propagate as unhandled exceptions.
Recommendation: Fix to `except (ValidationError, KeyError, ValueError):` and `except (ValueError, UnicodeDecodeError, binascii.Error):`.

---

## HIGH

### [HIGH-1] No EventType-to-Pydantic-model mapping exists

Services affected: event-schemas, event-receiver, event-saver
Location: `event-schemas/event_schemas/__init__.py`
Description: There is no programmatic mapping from `EventType` enum values to their corresponding Pydantic payload models. The event-receiver's normalizer uses ad-hoc `match` statements to select which model to validate. There is no way to look up "given this EventType, which schema should I validate against?" This makes it easy for new event types to be added to the enum without a corresponding model, or for models to exist without being wired to any event type.
Recommendation: Add an `EVENT_TYPE_TO_MODEL: dict[EventType, type[BaseModel]]` mapping in `event-schemas` and use it in event-receiver for dispatch.

---

### [HIGH-2] ~~GETSTREAM_CHANEL_CREATED/DELETED misspelled (should be CHANNEL)~~ — RESOLVED

Services affected: event-schemas, event-receiver
Location: `event-schemas/event_schemas/types.py`
Resolution: Enum members have been renamed to `GETSTREAM_CHANNEL_CREATED` and `GETSTREAM_CHANNEL_DELETED` (correct spelling). All references in event-receiver normalizers updated accordingly.

---

### [HIGH-3] ~~EVENT_PRIORITIES missing entries for GETSTREAM_CHANEL_CREATED and GETSTREAM_CHANEL_DELETED~~ — RESOLVED

Services affected: event-schemas, event-receiver
Location: `event-schemas/event_schemas/types.py`
Resolution: `EVENT_PRIORITIES` now has complete coverage — all 35 `EventType` members have explicit entries, including `GETSTREAM_CHANNEL_CREATED` and `GETSTREAM_CHANNEL_DELETED` (fixed in conjunction with HIGH-2 rename).

---

### [HIGH-4] ~~EVENT_SCHEMA_VERSIONS missing entries for GETSTREAM_CHANEL_CREATED and GETSTREAM_CHANEL_DELETED~~ — RESOLVED

Services affected: event-schemas, event-receiver
Location: `event-schemas/event_schemas/types.py`
Resolution: `EVENT_SCHEMA_VERSIONS` now has complete coverage — all 35 `EventType` members have explicit entries, including `GETSTREAM_CHANNEL_CREATED` and `GETSTREAM_CHANNEL_DELETED` (fixed in conjunction with HIGH-2 rename).

---

### [HIGH-5] event-notifier hardcodes TriggerEvent strings instead of using the shared enum

Services affected: event-schemas, event-notifier
Location: `event-notifier/event_notifier/event_types.py:9-15`
Description: `event-notifier` defines `DOMAIN_EVENT_TO_TRIGGER` with hardcoded string values like `"BOOKING_CREATED"` instead of using `TriggerEvent.BOOKING_CREATED.value` from `event-schemas`. The channel implementations (`email.py`, `telegram.py`, `push.py`) also use `trigger_event: str` rather than the `TriggerEvent` enum. If a TriggerEvent value changes in event-schemas, event-notifier will silently break.
Recommendation: Import and use `TriggerEvent` enum from `event-schemas` in event-notifier. Type `trigger_event` parameters as `TriggerEvent` or at minimum validate against it.

---

### [HIGH-6] NormalizedParticipant.email is `str`, not `EmailStr` -- no validation on normalized output

Services affected: event-schemas, event-receiver, event-saver
Location: `event-schemas/event_schemas/normalized.py:19`
Description: `NormalizedParticipant` is a `TypedDict` with `email: str`. Since TypedDicts have no runtime validation, email values flow through without any format check in the normalized payload. While upstream Pydantic models validate emails, the normalized structure strips that guarantee -- raw dict participants extracted from external payloads (GetStream, Jitsi, UniSender) bypass Pydantic validation entirely and feed `str` emails directly into the normalized structure.
Recommendation: Either validate email format in the normalizer before insertion, or document that normalized participants may contain unvalidated email strings.

---

## MEDIUM

### [MEDIUM-1] ~~No IANA timezone validator exists despite CLAUDE.md claiming one~~ — RESOLVED (audit-v2, 2026-06-11)

Services affected: event-schemas
Location: `event-schemas/event_schemas/types.py`, `event-schemas/CLAUDE.md:48`
Description: CLAUDE.md states "timezone fields use an IANA pattern validator," but no such validator exists anywhere in the codebase. `UserInfo` does not even have a `time_zone` field, and `NormalizedParticipant.time_zone` is typed as `str | None` with no validation.
Resolution: `TimeZoneName` (Annotated `str` with an `AfterValidator` that resolves the name via `zoneinfo.ZoneInfo`) is defined in `types.py` and applied to `UserInfo.time_zone` and `BookingParticipant.time_zone`. `EnvelopeParticipant.time_zone` stays a lenient `str | None` by design (consumer-side parsing must tolerate in-flight legacy messages). CLAUDE.md now describes the real mechanism.

---

### [MEDIUM-2] EVENT_SCHEMA_VERSIONS are cosmetic -- no runtime enforcement

Services affected: event-schemas, event-receiver
Location: `event-receiver/event_receiver/adapters/publisher.py:75`, `event-schemas/event_schemas/types.py:116-140`
Description: `EVENT_SCHEMA_VERSIONS` is used only to populate the `dataschema` CloudEvent attribute (line 75: `schema_version = EVENT_SCHEMA_VERSIONS.get(event_type_enum, "v1")`). The version string is embedded in the URI `https://schemas.example.com/{event_type}/{schema_version}` but never checked by any consumer. Event-saver ignores this attribute entirely. The versions are all `"v1"` with no mechanism to bump or enforce version compatibility.
Recommendation: Either implement version checking in consumers (reject unknown versions, handle migration), or remove `EVENT_SCHEMA_VERSIONS` to avoid false confidence. At minimum, document that versioning is not enforced.

---

### [MEDIUM-3] BookingRescheduledPayload not validated by event-receiver

Services affected: event-schemas, event-receiver
Location: `event-receiver/event_receiver/controllers/ingest.py:115-127`
Description: The ingest controller validates `BookingCreatedPayload` on line 118 but passes all other booking event types (including `booking.rescheduled`, `booking.reassigned`, `booking.cancelled`) through without schema validation (`else: payload_dict = incoming.data`). The normalizer validates some of these downstream, but `BookingRescheduledPayload` and `BookingCancelledPayload` are never validated against their Pydantic models anywhere in the pipeline.
Recommendation: Validate all booking event types against their respective schemas in the ingest controller, using an EventType-to-model mapping.

---

### [MEDIUM-4] event-saver missing BOOKING_RESCHEDULED from its EventType enum

Services affected: event-saver
Location: `event-saver/event_saver/event_types.py:20-37`
Description: event-saver's `EventType` enum includes `BOOKING_CREATED`, `BOOKING_CANCELLED`, `BOOKING_REASSIGNED`, and `BOOKING_REMINDER_SENT`, but has no `BOOKING_RESCHEDULED` member. The routing config at `event-saver/event_saver/config.py:18` routes `"booking.rescheduled"` events by pattern, but there is no typed enum member for this event type. This means rescheduled events are routed and stored but not typed in the enum, creating an inconsistency.
Recommendation: Add `BOOKING_RESCHEDULED` to event-saver's EventType enum.

---

### [MEDIUM-5] ~~GetStreamEventPayload uses both explicit `extra` field and `model_config extra="allow"`~~ — RESOLVED (audit-v2, 2026-06-11)

Services affected: event-schemas
Location: `event-schemas/event_schemas/external.py:28-52`
Description: `GetStreamEventPayload` declares an explicit `extra: dict[str, Any]` field AND sets `model_config = {"extra": "allow"}`. These serve different purposes: the explicit field captures known extras, while `extra="allow"` lets Pydantic accept any additional top-level fields. The result is confusing -- extra fields from the webhook end up in `model.__pydantic_extra__`, not in the explicit `extra` dict field. The explicit `extra` field is never populated by webhook data.
Resolution: The explicit `extra` field was removed from both `GetStreamEventPayload` and `JitsiEventPayload` (same defect); `extra="allow"` is the single mechanism — unknown upstream fields land in `model.__pydantic_extra__`. No producer or consumer ever populated/read the explicit field (verified by grep across event-receiver/saver/notifier/users/booking).

---

### [MEDIUM-6] ClientInfo and UserInfo are structurally identical -- no value in separate classes

Services affected: event-schemas
Location: `event-schemas/event_schemas/types.py:72-82`
Description: `UserInfo` and `ClientInfo` are identical Pydantic models with only `email: EmailStr`. `ClientInfo` docstring says "extends UserInfo for future fields" but does not actually inherit from `UserInfo`. If future fields are added to one but not the other, the lack of inheritance means the divergence must be tracked manually.
Recommendation: Make `ClientInfo` inherit from `UserInfo`, or merge them into a single `PersonInfo` class if the distinction is not meaningful.

---

## LOW

### [LOW-1] ~~No test suite for event-schemas~~ — RESOLVED (audit-v2, 2026-06-11)

Services affected: event-schemas
Location: `event-schemas/CLAUDE.md`
Description: CLAUDE.md explicitly states "No test suite exists -- this is a schema library relying on strict typing for correctness." However, several findings in this audit (missing fields, missing map entries, typos) demonstrate that typing alone does not catch all issues. Schema completeness, map coverage, and enum-to-model mapping are all testable properties.
Resolution: `tests/` now contains 73 tests: envelope round-trip + unwrap (`test_envelope.py`), queue/topology invariants (`test_queues.py`), payload-mapping basics (`test_mapping.py`), and contract completeness + wire-format fidelity (`test_payload_contracts.py`: every EventType has a payload model, priority and schema version; every mapped model's documented example round-trips through the canonical envelope JSON; validator behavior for `TimeZoneName`/`UuidStr`).

---

### [LOW-2] ~~BookingCreatedPayload.volunteer_id / client_id are `str`, not UUID-validated~~ — RESOLVED (audit-v2, 2026-06-11)

Services affected: event-schemas
Location: `event-schemas/event_schemas/booking.py:13-14`
Description: `volunteer_id` and `client_id` are typed as `str` with description "UUID" but no UUID format validation. Invalid UUID strings will pass validation.
Resolution: `UuidStr` (Annotated `str` validated via `uuid.UUID`) is applied to `BookingCreatedPayload.volunteer_id/client_id`, `BookingReminderSentPayload.client_id`, `UserEmailChangeRequestedPayload.user_id` and `BookingClientReassignedPayload.new_client_user_id`. Producer check (read-only): event-admin publishes real event-users UUIDs for `user_id`/`new_client_user_id`; cal.com webhooks observed in production (`event-booking/requests.jsonl`) never carry `volunteer_id`/`client_id`, and the fields stay optional, so pass-through ingest is unaffected. Wire format remains `str` (no breaking change).

---

### [LOW-3] BookingCancelledPayload missing user/client email fields

Services affected: event-schemas
Location: `event-schemas/event_schemas/booking.py:70-81`
Description: Unlike `BookingCreatedPayload` which includes `user` and `client` with emails, `BookingCancelledPayload` only has `volunteer_id`, `client_id`, and `cancellation_reason`. The normalizer uses the same extraction function as `booking.created` (line 61: `case EventType.BOOKING_CREATED | EventType.BOOKING_CANCELLED`) which expects `user.email` and `client.email`. This will fail at runtime for cancelled events that don't include the full user/client objects.
Recommendation: Either add `user` and `client` fields to `BookingCancelledPayload`, or use a separate normalizer path for cancelled events.

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 3 |
| HIGH | 6 |
| MEDIUM | 6 |
| LOW | 3 |
| **Total** | **18** |

**Top 3 concerns:**

1. **Dual EventType enums** (CRITICAL-1): event-saver maintains its own EventType with entirely different string values, defeating the purpose of a shared schema library. This is the most fundamental architectural issue.
2. **UserInfo missing time_zone** (CRITICAL-2) + **broken except syntax** (CRITICAL-3): Together these mean every `booking.reassigned` event silently drops participant data. The `AttributeError` from the missing field is not caught because the `except` clause only catches `ValidationError` (the comma syntax bug means `KeyError` becomes the binding variable, not a caught exception type).
3. **No EventType-to-model mapping** (HIGH-1) + **incomplete validation** (MEDIUM-3): Without a programmatic mapping, schema validation is ad-hoc and inconsistent. Only `booking.created` events are validated in the ingest controller; all other event types pass through unvalidated.

---

## Drift Matrix

| EventType (event-schemas) | Schema Model Defined? | Used in event-receiver? | Used in event-saver? | Notes |
|---|---|---|---|---|
| `booking.created` | BookingCreatedPayload | Validated in ingest + normalizer | Own enum (`booking.events.v1.booking.created.create`) | String mismatch |
| `booking.rescheduled` | BookingRescheduledPayload | Not validated | No enum member in event-saver | Missing from saver enum |
| `booking.reassigned` | BookingReassignedPayload | Normalizer only (broken -- see CRITICAL-2) | Own enum | AttributeError at runtime |
| `booking.cancelled` | BookingCancelledPayload | Normalizer reuses created path (schema mismatch) | Own enum | Missing user/client fields |
| `booking.reminder_sent` | BookingReminderSentPayload | Normalizer only | Own enum | OK |
| `chat.created` | ChatCreatedPayload | Not used | Routed by pattern only | No validation |
| `chat.deleted` | ChatDeletedPayload | Not used | Routed by pattern only | No validation |
| `chat.message_sent` | ChatMessageSentPayload | Not used | Routed by pattern only | No validation |
| `meeting.url_created` | MeetingUrlCreatedPayload | Normalizer (generic users list) | Own enum | No model validation |
| `meeting.url_deleted` | MeetingUrlDeletedPayload | Normalizer (generic users list) | Own enum | No model validation |
| `notification.email.message_sent` | EmailNotificationPayload | Normalizer (generic users list) | Own enum | No model validation |
| `notification.telegram.message_sent` | TelegramNotificationPayload | Normalizer (generic users list) | Own enum | No model validation |
| `notification.send_requested` | NotificationCommandPayload | Routed only | Not in saver enum | Consumed by event-notifier |
| `notification.push.message_sent` | PushNotificationPayload | Not used | Not in saver enum | No consumer |
| `unisender.events.v1.transactional.status.create` | UniSenderStatusPayload | Normalizer validated | Own enum (same string) | Only matching string value |
| `getstream.channel.created` | GetStreamEventPayload (shared) | Normalizer validated | Own enum (different string) | Enum name corrected (was CHANEL) |
| `getstream.channel.deleted` | GetStreamEventPayload (shared) | Normalizer validated | Own enum (different string) | Enum name corrected (was CHANEL) |
| `getstream.message.new` | GetStreamEventPayload (shared) | Normalizer validated | Own enum (different string) | String mismatch |
| `getstream.message.updated` | GetStreamEventPayload (shared) | Not used in normalizer | No saver enum member | No consumer |
| `getstream.message.deleted` | GetStreamEventPayload (shared) | Not used in normalizer | No saver enum member | No consumer |
| `getstream.message.read` | GetStreamEventPayload (shared) | Not used in normalizer | Own enum (different string) | String mismatch |
| `jitsi.conference.joined` | JitsiEventPayload (shared) | Normalizer validated | Matched by prefix pattern | No typed enum in saver |
| `jitsi.conference.left` | JitsiEventPayload (shared) | Normalizer validated | Matched by prefix pattern | No typed enum in saver |
| `jitsi.participant.joined` | JitsiEventPayload (shared) | Normalizer validated | Matched by prefix pattern | No typed enum in saver |
| `jitsi.participant.left` | JitsiEventPayload (shared) | Normalizer validated | Matched by prefix pattern | No typed enum in saver |
| `jitsi.participant.muted` | JitsiEventPayload (shared) | Not validated in normalizer | Matched by prefix pattern | No typed enum in saver |
| `jitsi.participant.menu_button_click` | JitsiEventPayload (shared) | Not validated in normalizer | Matched by prefix pattern | No typed enum in saver |
| `jitsi.audio.mute_status_changed` | JitsiEventPayload (shared) | Not validated in normalizer | Matched by prefix pattern | No typed enum in saver |
| `jitsi.video.mute_status_changed` | JitsiEventPayload (shared) | Not validated in normalizer | Matched by prefix pattern | No typed enum in saver |
| `jitsi.speaker.dominant_changed` | JitsiEventPayload (shared) | Not validated in normalizer | Matched by prefix pattern | No typed enum in saver |
| `jitsi.device.list_changed` | JitsiEventPayload (shared) | Not validated in normalizer | Matched by prefix pattern | No typed enum in saver |
| `jitsi.camera.error` | JitsiEventPayload (shared) | Not validated in normalizer | Matched by prefix pattern | No typed enum in saver |
| `jitsi.mic.error` | JitsiEventPayload (shared) | Not validated in normalizer | Matched by prefix pattern | No typed enum in saver |
| `jitsi.error.occurred` | JitsiEventPayload (shared) | Not validated in normalizer | Matched by prefix pattern | No typed enum in saver |
| `jitsi.peer_connection.failure` | JitsiEventPayload (shared) | Not validated in normalizer | Matched by prefix pattern | No typed enum in saver |
| `jitsi.suspend.detected` | JitsiEventPayload (shared) | Not validated in normalizer | Matched by prefix pattern | No typed enum in saver |
| `jitsi.toolbar.button_clicked` | JitsiEventPayload (shared) | Not validated in normalizer | Matched by prefix pattern | No typed enum in saver |
| -- | EmailRejectionNotificationPayload | Not wired to any EventType | Not used | Orphaned model |

**Legend:** "Own enum" = event-saver has its own EventType member with a different string value than event-schemas.
