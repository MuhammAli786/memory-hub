# Second Brain Platform

## Goal

Maintain a private, sourced knowledge system that captures agent work, curates
approved source material, supports memory retrieval, and exposes code and wiki
relationships to coding agents.

## Automation

- Session hooks capture L0 and inject reviewed, fresh context.
- A scheduler sweeps missed sessions.
- Source intake and queue creation run on an approved cadence.
- A reviewed ingest worker updates wiki pages and the activity log.
- Stale-page reporting identifies pages needing review; it never rewrites them.
- One graph worker rebuilds the graph snapshot.
- A controlled container reconciler maintains the memory, knowledge, and panel
  deployment only when explicitly applied.

## Acceptance Checks

- Raw material remains immutable.
- Every durable wiki claim has a source.
- Memory capture is idempotent and fail-open.
- Private repository graph access is read-only and least-privilege.
- No credential, personal data, or live routing value is committed.
