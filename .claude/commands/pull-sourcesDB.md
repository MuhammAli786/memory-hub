---
description: Collect approved source exports and prepare them for private knowledge ingestion
argument-hint: "[source name]"
---

Run only the explicitly configured source connector. Apply its inclusion, exclusion, deduplication, and volume controls before writing anything under `raw/`. Report written, filtered, and duplicate counts. Append the result to the activity log, inspect the ingest queue, and ask before starting `/ingestDB`; a long ingest is a separate state-changing operation.
