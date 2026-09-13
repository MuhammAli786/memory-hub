---
description: Pull approved user-owned exports into raw sources and refresh the review queue
argument-hint: "[connector name | status]"
---

# Pull Sources DB

1. Read only an explicitly configured private connector. If absent, report
   `BLOCKED`; never invent accounts, credentials, paths, or source scope.
2. Apply consent, filters, date range, volume limits, and deduplication before
   creating raw files.
3. Preserve source provenance and a stable identity; do not rewrite old sources.
4. Run `tools/source_intake.py` and update the private local manifest.
5. Run `tools/ingest_queue.py` to classify material without a model.
6. Report written, filtered, duplicate, thin, ready, and review-large counts.
7. Append activity and ask before invoking `/ingestDB`.

Collection and curation are separate state changes. Never chain them silently.
