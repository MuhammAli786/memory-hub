---
name: code-graph
description: Build and query a durable relationship graph over a second-brain vault while preserving freshness and single-writer ownership.
---

# Code Graph

Build the structural baseline with `tools/build_code_graph.py`. Use a richer Graphify workflow when available. The graph combines wiki content, conversation material, and implementation structure, but it is a retrieval index—not the source of truth.

There must be one designated graph writer. Store source inventory and generation time in every snapshot. Validate fragment-local facts while extracting; resolve cross-fragment references after merge. Do not treat a generic ready status as freshness. Before changing code or recording a claim, open the current source that a graph result points to.
