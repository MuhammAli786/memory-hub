---
name: second-brain-operations
description: >-
  Operate a sourced second-brain vault through raw-source intake, curation,
  memory-aware query, activity logging, briefing, debrief, and triage. Use for
  ingest, pull sources, log, query, briefing, debrief, or triage requests.
---

# Second Brain Operations

## Required reading order

Before acting, read `CLAUDE.md`, `priorities.md`, recent `wiki/activity-log.md`,
and the matching `.claude/commands/` procedure. Search existing wiki pages and
memory before re-deriving a decision. An empty result can signal a scope or
service problem; do not convert it into a claim that information is absent.

## Data ownership

| Layer | Owner | Rule |
| --- | --- | --- |
| `raw/` | source connector or user | Input-only; never rewrite or reorganize |
| `wiki/` | agent with review | Curated, sourced, atomic knowledge |
| `wiki/activity-log.md` | append-only workflow | Record material work and outcomes |
| `wiki/log.md` | ingest engine | Never place vault knowledge here |
| L0/L1/L2 | private memory service | Retrieval support, not automatic wiki truth |

## Pull sources and ingest

Run only configured connectors. Apply consent, source-specific filters,
deduplication, and volume limits before writing raw files. Report written,
filtered, duplicate, and deferred counts; ask before ingestion.

Reject empty, near-empty, duplicate, and malformed input before any model call.
Route bounded sources to an approved model and flag oversized or ambiguous
material for review. Search the wiki first. Create only pages supported by the
source, using exact names/numbers, source attribution, explicit contradictions,
and the page template. Update the index and activity log. Verify a private
knowledge mirror before claiming two stores are synchronized.

## LogDB and QueryDB

The activity log is append-only. Record what was processed, created, updated,
deferred, failed, or verified—never an outcome that has not happened. Use one
reviewed atomic adapter operation if a private knowledge-store copy exists.

Query in order: wiki for curated knowledge; L1 for decisions; L0 for original
wording; L2 for work-period context; graph for relationships. Cite sources and
distinguish fact from inference. A graph result is a lead; open current sources
before consequential work.

## Briefing, debrief, triage, and stop conditions

Brief from priorities, activity, and evidence—not generic advice. Debrief into
three to five durable signal bullets: shift, decision, blocker, carry-forward.
Propose a new page or priority change where a choice is required; never silently
alter either. Triage as ingest, defer, duplicate, or noise without deleting raw
material. Stop and report if a source is unavailable, a store is not ready, the
same action fails twice, or a requested write needs approval.
