---
description: Append a verified activity record to the local and private knowledge stores
argument-hint: "<note>"
---

Append the note locally with `tools/append_activity.py`. If a private knowledge adapter is configured, invoke its reviewed atomic append operation before reporting success. Do not write directly to `wiki/log.md`. The activity log is append-only; update an existing referenced page separately when its state changed.
