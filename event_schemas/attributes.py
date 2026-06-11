"""Canonical CloudEvent extension attribute names.

CloudEvents extension attribute names MUST be lowercase alphanumeric
(no underscores), so the canonical booking identifier attribute is
``bookingid`` (HTTP/AMQP binary-mode header ``ce-bookingid``).

Every producer and consumer MUST use these constants instead of literals.
"""

CE_HEADER_PREFIX = "ce-"

BOOKING_ID_ATTRIBUTE = "bookingid"
TRACE_ID_ATTRIBUTE = "traceid"
SPAN_ID_ATTRIBUTE = "spanid"
IDEMPOTENCY_KEY_ATTRIBUTE = "idempotencykey"

BOOKING_ID_HEADER = f"{CE_HEADER_PREFIX}{BOOKING_ID_ATTRIBUTE}"
TRACE_ID_HEADER = f"{CE_HEADER_PREFIX}{TRACE_ID_ATTRIBUTE}"
SPAN_ID_HEADER = f"{CE_HEADER_PREFIX}{SPAN_ID_ATTRIBUTE}"
IDEMPOTENCY_KEY_HEADER = f"{CE_HEADER_PREFIX}{IDEMPOTENCY_KEY_ATTRIBUTE}"
