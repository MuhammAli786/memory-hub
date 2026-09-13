---
name: code-graph
description: >-
  Build, refresh, and query a relationship graph over code, wiki pages, and
  selected conversations. Use for architecture questions, caller tracing,
  graph refreshes, impact analysis, or questions asking how components relate.
---

# Code Graph

## Purpose and inputs

The graph is a retrieval and navigation layer, not the source of truth.

```text
approved wiki pages + selected L0 conversations + repository source
  → normalize identifiers → chunk → extract → merge → label → graph snapshot
  → Graphify MCP and code-graph queries
```

Use `python3 tools/build_code_graph.py --root . --output graphify-out/graph.json`
for the structural baseline. Use Graphify when richer multi-language or document
relationships are needed.

## Ownership and freshness

There is exactly one designated graph writer. Other machines may read, copy, or
commit a completed snapshot, but must not concurrently rebuild the same output.
Every snapshot needs a generation time and input inventory. Never infer
freshness from a status field or modification time alone.

## Extraction rules

1. Reject empty input and record skipped material.
2. Extract code facts deterministically where possible.
3. Let a model propose document relationships only when source text is present.
4. Require exact source identifiers; never accept invented node IDs.
5. Validate fragment-local facts while extracting, but resolve cross-fragment
   references only after all chunks merge.
6. Keep unresolved edges visible instead of silently deleting or guessing a
   target. Label communities after structural merge; labels are summaries.

## Query and failure workflow

Query for relationships, paths, neighbourhoods, callers, or important nodes;
then check snapshot freshness and open current sources for consequential work.
State whether a conclusion is extracted, inferred, or uncertain. If extraction
or merge returns the same error twice, stop and report the blocker. If graph
size unexpectedly shrinks, preserve the prior snapshot and investigate input
inventory before publishing the new one.
