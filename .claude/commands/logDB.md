---
description: Append a verified activity record locally and through the private knowledge adapter
argument-hint: "<factual note>"
---

# LogDB

Record only completed, evidence-backed work: changes, verification, failure,
remaining work, and page links. The activity log is not a plan, secret store,
or model scratchpad.

1. Locate any affected wiki page and update it only when evidence supports it.
2. Bump `last-updated`, lint the page, and append once with
   `tools/append_activity.py --log wiki/activity-log.md`.
3. Mirror via the private adapter’s atomic append only when configured, and
   verify its outcome before reporting synchronization.
4. Never alter prior entries or write vault content to `wiki/log.md`.
