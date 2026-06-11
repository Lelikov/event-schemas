# event-schemas: API Contracts

All exports are defined in `event_schemas/__init__.py:44-83`.

---

## Enums

### SourceType (`types.py:8-14`)

`StrEnum`. Identifies the originating system of a CloudEvent (used as the `ce-source` attribute).

| Member | Value |
|--------|-------|
| `BOOKING` | `"booking"` |
| `GETSTREAM` | `"getstream"` |
| `UNISENDER_GO` | `"unisender-go"` |
| `JITSI` | `"jitsi"` |

### EventType (`types.py:17-65`)

`str` enum. Values are dot-delimited event identifiers used as CloudEvent `ce-type`.

| Member | Value |
|--------|-------|
| `BOOKING_CREATED` | `"booking.created"` |
| `BOOKING_RESCHEDULED` | `"booking.rescheduled"` |
| `BOOKING_REASSIGNED` | `"booking.reassigned"` |
| `BOOKING_CANCELLED` | `"booking.cancelled"` |
| `BOOKING_REMINDER_SENT` | `"booking.reminder_sent"` |
| `CHAT_CREATED` | `"chat.created"` |
| `CHAT_DELETED` | `"chat.deleted"` |
| `CHAT_MESSAGE_SENT` | `"chat.message_sent"` |
| `MEETING_URL_CREATED` | `"meeting.url_created"` |
| `MEETING_URL_DELETED` | `"meeting.url_deleted"` |
| `NOTIFICATION_EMAIL_SENT` | `"notification.email.message_sent"` |
| `NOTIFICATION_TELEGRAM_SENT` | `"notification.telegram.message_sent"` |
| `NOTIFICATION_SEND_REQUESTED` | `"notification.send_requested"` |
| `NOTIFICATION_PUSH_SENT` | `"notification.push.message_sent"` |
| `UNISENDER_STATUS_CREATED` | `"unisender.events.v1.transactional.status.create"` |
| `GETSTREAM_CHANNEL_CREATED` | `"getstream.channel.created"` |
| `GETSTREAM_CHANNEL_DELETED` | `"getstream.channel.deleted"` |
| `GETSTREAM_MESSAGE_NEW` | `"getstream.message.new"` |
| `GETSTREAM_MESSAGE_UPDATED` | `"getstream.message.updated"` |
| `GETSTREAM_MESSAGE_DELETED` | `"getstream.message.deleted"` |
| `GETSTREAM_MESSAGE_READ` | `"getstream.message.read"` |
| `JITSI_CONFERENCE_JOINED` | `"jitsi.conference.joined"` |
| `JITSI_CONFERENCE_LEFT` | `"jitsi.conference.left"` |
| `JITSI_PARTICIPANT_JOINED` | `"jitsi.participant.joined"` |
| `JITSI_PARTICIPANT_LEFT` | `"jitsi.participant.left"` |
| `JITSI_PARTICIPANT_MUTED` | `"jitsi.participant.muted"` |
| `JITSI_PARTICIPANT_MENU_BUTTON_CLICK` | `"jitsi.participant.menu_button_click"` |
| `JITSI_AUDIO_MUTE_STATUS_CHANGED` | `"jitsi.audio.mute_status_changed"` |
| `JITSI_VIDEO_MUTE_STATUS_CHANGED` | `"jitsi.video.mute_status_changed"` |
| `JITSI_SPEAKER_DOMINANT_CHANGED` | `"jitsi.speaker.dominant_changed"` |
| `JITSI_DEVICE_LIST_CHANGED` | `"jitsi.device.list_changed"` |
| `JITSI_CAMERA_ERROR` | `"jitsi.camera.error"` |
| `JITSI_MIC_ERROR` | `"jitsi.mic.error"` |
| `JITSI_ERROR_OCCURRED` | `"jitsi.error.occurred"` |
| `JITSI_PEER_CONNECTION_FAILURE` | `"jitsi.peer_connection.failure"` |
| `JITSI_SUSPEND_DETECTED` | `"jitsi.suspend.detected"` |
| `JITSI_TOOLBAR_BUTTON_CLICKED` | `"jitsi.toolbar.button_clicked"` |

### EventPriority (`types.py:46-52`)

`int` enum used for RabbitMQ message priority.

| Member | Value |
|--------|-------|
| `CRITICAL` | `10` |
| `HIGH` | `7` |
| `NORMAL` | `5` |
| `LOW` | `1` |

### RecipientRole (`types.py:55-59`)

`str` enum.

| Member | Value |
|--------|-------|
| `ORGANIZER` | `"organizer"` |
| `CLIENT` | `"client"` |

### TriggerEvent (`types.py:62-70`)

`str` enum. Identifies which booking lifecycle event triggered a notification.

| Member | Value |
|--------|-------|
| `BOOKING_CREATED` | `"BOOKING_CREATED"` |
| `BOOKING_RESCHEDULED` | `"BOOKING_RESCHEDULED"` |
| `BOOKING_REASSIGNED` | `"BOOKING_REASSIGNED"` |
| `BOOKING_CANCELLED` | `"BOOKING_CANCELLED"` |
| `BOOKING_REMINDER` | `"BOOKING_REMINDER"` |
| `BOOKING_REJECTED` | `"BOOKING_REJECTED"` |

---

## Base Models (`types.py`)

### UserInfo (`types.py:73-77`)

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `email` | `EmailStr` | required | |
| `time_zone` | `TimeZoneName \| None` | `None` | IANA timezone, validated against the zoneinfo database |

### ClientInfo (`types.py:80-83`)

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `email` | `EmailStr` | required | Inherits from UserInfo (email + time_zone) |

---

## Booking Payloads (`booking.py`)

### BookingCreatedPayload (`booking.py:10-31`)

| Field | Type | Default |
|-------|------|---------|
| `volunteer_id` | `UuidStr \| None` | `None` |
| `client_id` | `UuidStr \| None` | `None` |
| `user` | `UserInfo` | required |
| `client` | `ClientInfo` | required |
| `start_time` | `datetime` | required |
| `end_time` | `datetime` | required |

### BookingRescheduledPayload (`booking.py:34-56`)

| Field | Type | Default |
|-------|------|---------|
| `volunteer_id` | `str` | required |
| `client_id` | `str` | required |
| `start_time` | `datetime` | required |
| `end_time` | `datetime` | required |
| `previous_booking` | `dict[str, datetime \| None]` | `{}` |

### BookingReassignedPayload (`booking.py:59-79`)

| Field | Type | Default |
|-------|------|---------|
| `volunteer_id` | `str` | required |
| `client_id` | `str` | required |
| `previous_organizer` | `dict[str, str \| None]` | `{}` |
| `user` | `UserInfo` | required |

### BookingCancelledPayload (`booking.py:82-97`)

| Field | Type | Default |
|-------|------|---------|
| `volunteer_id` | `str` | required |
| `client_id` | `str` | required |
| `cancellation_reason` | `str \| None` | `None` |

Note: Missing `user`/`client` fields that the normalizer expects (audit LOW-3).

### BookingReminderSentPayload (`booking.py:100-113`)

| Field | Type | Default |
|-------|------|---------|
| `client_id` | `UuidStr \| None` | `None` |
| `email` | `EmailStr` | required |

---

## Chat Payloads (`chat.py`)

### ChatCreatedPayload (`chat.py:6-19`)

| Field | Type | Default |
|-------|------|---------|
| `organizer_id` | `str` | required |
| `client_id` | `str` | required |

### ChatDeletedPayload (`chat.py:22-26`)

Empty model. Booking ID is conveyed via CloudEvent `ce-booking_id` attribute.

### ChatMessageSentPayload (`chat.py:29-34`)

| Field | Type | Default |
|-------|------|---------|
| `user_id` | `str` | required |

---

## Meeting Payloads (`meeting.py`)

### MeetingUrlCreatedPayload (`meeting.py:8-23`)

| Field | Type | Default |
|-------|------|---------|
| `email` | `EmailStr` | required |
| `recipient_role` | `RecipientRole` | required |
| `meeting_url` | `AnyHttpUrl` | required |

### MeetingUrlDeletedPayload (`meeting.py:26-31`)

| Field | Type | Default |
|-------|------|---------|
| `recipient_role` | `RecipientRole` | required |

---

## Notification Payloads (`notification.py`)

### EmailNotificationPayload (`notification.py:11-28`)

| Field | Type | Default |
|-------|------|---------|
| `email` | `EmailStr` | required |
| `job_id` | `str \| None` | `None` |
| `recipient_role` | `RecipientRole` | required |
| `trigger_event` | `TriggerEvent` | required |

### EmailRejectionNotificationPayload (`notification.py:31-62`)

| Field | Type | Default |
|-------|------|---------|
| `client_email` | `EmailStr` | required |
| `job_id` | `str \| None` | `None` |
| `available_from` | `datetime` | required |
| `has_active_booking` | `bool` | required |
| `active_booking_start` | `datetime \| None` | `None` |
| `previous_meeting_dates` | `list[datetime]` | `[]` |
| `rejection_reasons` | `list[str]` | `[]` |
| `trigger_event` | `TriggerEvent` | `TriggerEvent.BOOKING_REJECTED` |

Note: Orphaned -- not wired to any `EventType` member.

### TelegramNotificationPayload (`notification.py:65-83`)

| Field | Type | Default |
|-------|------|---------|
| `email` | `EmailStr` | required |
| `recipient_role` | `RecipientRole` | `RecipientRole.ORGANIZER` |
| `trigger_event` | `TriggerEvent` | required |

### NotificationRecipient (`notification.py:86-99`)

| Field | Type | Default |
|-------|------|---------|
| `email` | `EmailStr` | required |
| `role` | `RecipientRole` | required |

### NotificationCommandPayload (`notification.py:102-132`)

| Field | Type | Default |
|-------|------|---------|
| `booking_id` | `str` | required |
| `trigger_event` | `TriggerEvent` | required |
| `recipients` | `list[NotificationRecipient]` | required |
| `template_data` | `dict[str, Any]` | `{}` |

### PushNotificationPayload (`notification.py:135-154`)

| Field | Type | Default |
|-------|------|---------|
| `email` | `EmailStr` | required |
| `recipient_role` | `RecipientRole` | required |
| `trigger_event` | `TriggerEvent` | required |
| `device_token` | `str` | required |
| `message_id` | `str \| None` | `None` |

---

## External Payloads (`external.py`)

All models in this module use `model_config = {"extra": "allow"}` to accept arbitrary fields from third-party webhooks. Unknown top-level fields land in `model.__pydantic_extra__`; there is no explicit `extra` field (audit MEDIUM-5 resolved: single mechanism).

### UniSenderStatusPayload (`external.py:8-29`)

| Field | Type | Default |
|-------|------|---------|
| `event_name` | `str \| None` | `None` |
| `event_data` | `dict[str, Any]` | `{}` |

### GetStreamEventPayload (`external.py:32-58`)

| Field | Type | Default |
|-------|------|---------|
| `type` | `str` | required |
| `channel_id` | `str \| None` | `None` |
| `user` | `dict[str, Any] \| None` | `None` |
| `message` | `dict[str, Any] \| None` | `None` |
| `members` | `list[dict] \| None` | `None` |

Config: `extra = "allow"` -- additional webhook fields accepted at top level.

### JitsiEventPayload (`external.py:61-82`)

| Field | Type | Default |
|-------|------|---------|
| `room` | `str \| None` | `None` |
| `event_type` | `str \| None` | `None` |

Config: `extra = "allow"` -- additional JWT claim fields accepted at top level.

---

## Normalized Structures (`normalized.py`)

These are `TypedDict` classes. They provide structural typing only -- **no runtime validation occurs** when constructing these dicts.

### NormalizedParticipant (`normalized.py:16-22`)

| Key | Type | Required |
|-----|------|----------|
| `email` | `str` | yes |
| `role` | `str \| None` | no (`NotRequired`) |
| `time_zone` | `str \| None` | no (`NotRequired`) |
| `user_id` | `str` | no (`NotRequired`) |

### NormalizedBooking (`normalized.py:25-30`)

| Key | Type | Required |
|-----|------|----------|
| `start_time` | `str \| None` | no (`NotRequired`) |
| `end_time` | `str \| None` | no (`NotRequired`) |
| `status` | `str \| None` | no (`NotRequired`) |

### NormalizedData (`normalized.py:33-37`)

| Key | Type | Required |
|-----|------|----------|
| `participants` | `list[NormalizedParticipant]` | yes |
| `booking` | `NormalizedBooking` | yes |

### NormalizedPayload (`normalized.py:40-47`)

| Key | Type | Required |
|-----|------|----------|
| `original` | `dict` | yes |
| `normalized` | `NormalizedData` | yes |

---

## Constant Maps

### EVENT_PRIORITIES (`types.py:87-116`)

Complete mapping from every `EventType` member to an `EventPriority` value.

| EventType | Priority |
|-----------|----------|
| `BOOKING_CREATED` | CRITICAL (10) |
| `BOOKING_RESCHEDULED` | CRITICAL (10) |
| `BOOKING_REASSIGNED` | CRITICAL (10) |
| `BOOKING_CANCELLED` | CRITICAL (10) |
| `BOOKING_REMINDER_SENT` | HIGH (7) |
| `NOTIFICATION_EMAIL_SENT` | HIGH (7) |
| `NOTIFICATION_TELEGRAM_SENT` | HIGH (7) |
| `NOTIFICATION_SEND_REQUESTED` | HIGH (7) |
| `NOTIFICATION_PUSH_SENT` | HIGH (7) |
| `CHAT_CREATED` | NORMAL (5) |
| `CHAT_DELETED` | NORMAL (5) |
| `CHAT_MESSAGE_SENT` | NORMAL (5) |
| `MEETING_URL_CREATED` | NORMAL (5) |
| `MEETING_URL_DELETED` | NORMAL (5) |
| `UNISENDER_STATUS_CREATED` | NORMAL (5) |
| `GETSTREAM_CHANNEL_CREATED` | NORMAL (5) |
| `GETSTREAM_CHANNEL_DELETED` | NORMAL (5) |
| `GETSTREAM_MESSAGE_NEW` | NORMAL (5) |
| `GETSTREAM_MESSAGE_UPDATED` | NORMAL (5) |
| `GETSTREAM_MESSAGE_DELETED` | NORMAL (5) |
| `GETSTREAM_MESSAGE_READ` | NORMAL (5) |
| `JITSI_CONFERENCE_JOINED` | NORMAL (5) |
| `JITSI_CONFERENCE_LEFT` | NORMAL (5) |
| `JITSI_PARTICIPANT_JOINED` | NORMAL (5) |
| `JITSI_PARTICIPANT_LEFT` | NORMAL (5) |
| `JITSI_PARTICIPANT_MUTED` | NORMAL (5) |
| `JITSI_PARTICIPANT_MENU_BUTTON_CLICK` | NORMAL (5) |
| `JITSI_AUDIO_MUTE_STATUS_CHANGED` | NORMAL (5) |
| `JITSI_VIDEO_MUTE_STATUS_CHANGED` | NORMAL (5) |
| `JITSI_SPEAKER_DOMINANT_CHANGED` | NORMAL (5) |
| `JITSI_DEVICE_LIST_CHANGED` | NORMAL (5) |
| `JITSI_CAMERA_ERROR` | NORMAL (5) |
| `JITSI_MIC_ERROR` | NORMAL (5) |
| `JITSI_ERROR_OCCURRED` | NORMAL (5) |
| `JITSI_PEER_CONNECTION_FAILURE` | NORMAL (5) |
| `JITSI_SUSPEND_DETECTED` | NORMAL (5) |
| `JITSI_TOOLBAR_BUTTON_CLICKED` | NORMAL (5) |

### EVENT_SCHEMA_VERSIONS (`types.py:119-145`)

Complete mapping from every `EventType` member to a version string. All values are currently `"v1"`.

| EventType | Version |
|-----------|---------|
| `BOOKING_CREATED` | `v1` |
| `BOOKING_RESCHEDULED` | `v1` |
| `BOOKING_REASSIGNED` | `v1` |
| `BOOKING_CANCELLED` | `v1` |
| `BOOKING_REMINDER_SENT` | `v1` |
| `CHAT_CREATED` | `v1` |
| `CHAT_DELETED` | `v1` |
| `CHAT_MESSAGE_SENT` | `v1` |
| `MEETING_URL_CREATED` | `v1` |
| `MEETING_URL_DELETED` | `v1` |
| `NOTIFICATION_EMAIL_SENT` | `v1` |
| `NOTIFICATION_TELEGRAM_SENT` | `v1` |
| `NOTIFICATION_SEND_REQUESTED` | `v1` |
| `NOTIFICATION_PUSH_SENT` | `v1` |
| `UNISENDER_STATUS_CREATED` | `v1` |
| `GETSTREAM_CHANNEL_CREATED` | `v1` |
| `GETSTREAM_CHANNEL_DELETED` | `v1` |
| `GETSTREAM_MESSAGE_NEW` | `v1` |
| `GETSTREAM_MESSAGE_UPDATED` | `v1` |
| `GETSTREAM_MESSAGE_DELETED` | `v1` |
| `GETSTREAM_MESSAGE_READ` | `v1` |
| `JITSI_CONFERENCE_JOINED` | `v1` |
| `JITSI_CONFERENCE_LEFT` | `v1` |
| `JITSI_PARTICIPANT_JOINED` | `v1` |
| `JITSI_PARTICIPANT_LEFT` | `v1` |
| `JITSI_PARTICIPANT_MUTED` | `v1` |
| `JITSI_PARTICIPANT_MENU_BUTTON_CLICK` | `v1` |
| `JITSI_AUDIO_MUTE_STATUS_CHANGED` | `v1` |
| `JITSI_VIDEO_MUTE_STATUS_CHANGED` | `v1` |
| `JITSI_SPEAKER_DOMINANT_CHANGED` | `v1` |
| `JITSI_DEVICE_LIST_CHANGED` | `v1` |
| `JITSI_CAMERA_ERROR` | `v1` |
| `JITSI_MIC_ERROR` | `v1` |
| `JITSI_ERROR_OCCURRED` | `v1` |
| `JITSI_PEER_CONNECTION_FAILURE` | `v1` |
| `JITSI_SUSPEND_DETECTED` | `v1` |
| `JITSI_TOOLBAR_BUTTON_CLICKED` | `v1` |
