---
name: second-brain-operations
description: Operate a sourced second-brain vault through raw-source intake, wiki curation, activity logging, briefings, debriefs, and private-memory retrieval.
---

# Second Brain Operations

Use `raw/` as read-only input and `wiki/` as the curated layer. Read `CLAUDE.md`, `priorities.md`, and recent `wiki/activity-log.md` before an operation.

## Intake and ingestion

Reject empty, duplicate, and near-empty source material before using a model. Search existing wiki pages before creating a new one. Write sourced, atomic pages using the page template, update the index, and append an activity record. A private knowledge adapter may mirror only approved pages.

## LogDB

Append a timestamped factual record. Never alter prior entries. Keep the local log and private knowledge copy synchronized through one atomic adapter action; never write vault content to the engine-owned ingest log.

## QueryDB

Use wiki search for curated knowledge, L1 for decisions, L0 for original wording, L2 for narrative context, and the graph for relationships. Search results are leads; verify important claims against sources. Empty results may be a scope or service problem.

## BriefingDB and DebriefDB

Brief from active priorities and evidence, not generic productivity advice. Debrief with only durable signal. Propose a new page or priority edit when a choice is required; do not silently create or alter it.

## TriageDB

Classify but do not delete raw material. Prefer deferral over an unsupported conclusion.
