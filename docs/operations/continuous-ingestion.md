# Continuous Memory and Wiki Lifecycle

```text
SessionStart → private retrieval adapter → recall policy → additional context
Stop / SessionEnd → capture policy → private persistence adapter → L0 records
L0 records → extraction worker → L1 facts and L2 scenes
source exports → reviewed ingestion workflow → sourced wiki pages
wiki updates → activity log + index update → code-graph refresh
```

## Session hooks

`hooks/run_capture.py` selects substantive user/assistant pairs, applies a tail window before deduplication, and emits an offline batch. Its two stable identities prevent double writes after transcript changes. It always succeeds so a capture problem cannot trap a user in a session.

`hooks/recall_hook.py` accepts supplied L0/L1/L2 data and renders only reviewed persona content plus recent, dated dynamic material. It fails open with an empty result when input is unavailable or malformed.

## Webhook and adapter responsibilities

The host supplies a lifecycle envelope. A private adapter validates the event, resolves the transcript safely, applies user-controlled identity and authorisation, and persists accepted L0 records. The public hook scripts never hold a connection, credential, or identity.

## Wiki ingestion

Do not convert every chat event into a wiki page. Raw exports are queued under `raw/`; `/ingestDB` filters empty input, requires provenance, creates atomic pages, updates the index, and records the result. A scheduled runner may invoke that command, but it must use the same source-quality and activity-log rules as a manual run.
