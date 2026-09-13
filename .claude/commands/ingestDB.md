---
description: Curate approved raw sources into the database-backed wiki
argument-hint: "[source folder | status | review]"
---

# IngestDB

Use only after source intake has produced a reviewed queue. This is the sole
workflow that may turn material in `raw/` into durable wiki pages.

1. Read `CLAUDE.md`, priorities, recent activity, and the queue manifest.
2. For `status`, report queue counts by state and stop without writing.
3. Reject empty, duplicate, malformed, or provenance-free sources before any
   model call. Never alter the raw source.
4. Search private and local wiki for an existing page before creating one.
5. Route bounded sources to an approved model under the model-lane policy.
   Split or defer large, mixed, or ambiguous material.
6. Verify candidate claims against source text; preserve exact identifiers,
   names, dates, versions, and numbers. Omit unstated facts.
7. Write atomic pages with required frontmatter, source paths, contradictions,
   and valid wiki links. Never overwrite protected human-authored pages.
8. Rebuild the index, lint, then invoke a private knowledge adapter only if it
   returns a verified write outcome.
9. Append activity with source/page counts, failures, and deferrals.

Return `BLOCKED` for an unready store, repeated error, unverified identifier,
or write requiring user approval.
