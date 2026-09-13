---
description: Classify raw material before model-assisted ingestion
---

# TriageDB

Inspect queue metadata and representative source text. Classify each candidate
as `ingest`, `defer`, `duplicate`, `noise`, `split-required`, or `needs-review`.
Use provenance, source quality, novelty, and relation to stated priorities; do
not classify from a filename or model confidence alone. Never delete raw
material. Record only decisions that change the queue or future workflow.
