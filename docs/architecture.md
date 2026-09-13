# Architecture

The design separates durable knowledge from transient execution context.

```text
session host
  ├── session-start hook → retrieval adapter → approved context block
  ├── stop hook          → capture adapter   → L0 transcript records
  └── session-end hook   → capture adapter   → final flush

memory service
  ├── L0: source conversation turns
  ├── L1: extracted facts and decisions
  └── L2: summaries of periods of work

knowledge service
  ├── wiki pages and source provenance
  └── code-graph metadata

MCP aggregation layer
  └── progressive discovery → curated read-only operations
```

## Ownership boundaries

The hook layer owns transcript parsing, turn selection, deterministic deduplication, and fail-open behavior. The memory layer owns extraction and persistence. The retrieval adapter owns identity and authorization. The MCP layer owns tool discovery, sandboxing, response shaping, and the allow-list. Keeping these boundaries separate prevents a session hook from becoming an unauditable deployment client.

## Data lifecycle

L0 preserves source turns. L1 stores extracted facts only after a model or reviewer has produced them. L2 is a time-bounded narrative index; it is a pointer for follow-up reading, not a replacement for source material. A wiki is a separately curated knowledge layer with source links. Code graphs are snapshots and must carry an explicit freshness field.

## Safety properties

- Hooks fail open: capture failure must never prevent a session from ending.
- Two identities per turn avoid duplicate writes after transcript rewrites.
- Selection applies the cap before deduplication so repeated runs cannot slowly ingest older history.
- Session-start injection is time-bounded; stale information remains retrievable but is not silently presented as current.
- The MCP catalog excludes destructive operations by default.
