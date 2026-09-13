# Lifecycle Webhook Contract

The reference hook interface has three event names: `session.start`, `session.stop`, and `session.end`. The event name is metadata, not an authentication mechanism.

## Input envelope

```json
{
  "event": "session.stop",
  "session_id": "opaque-session-id",
  "transcript_path": "caller-managed-path",
  "project": "optional-project-label",
  "occurred_at": "ISO-8601 timestamp"
}
```

Required keys are `event` and `session_id`. `transcript_path` is required by capture events. The host must validate paths before invoking a hook.

## Capture output

```json
{
  "session_id": "opaque-session-id",
  "accepted": [{"turn_id": "sha256", "content_hash": "sha256", "user": "text", "assistant": "text"}],
  "skipped": {"empty": 0, "short": 0, "known": 0, "outside_tail": 0}
}
```

The hook does not define an authorization header, signature key, or endpoint. Those belong to the external adapter and must be managed outside version control.

## Context-injection output

```json
{"additionalContext": "reviewed and freshness-gated text"}
```

An unavailable retrieval dependency returns an empty object and a successful process status. This preserves session availability.
