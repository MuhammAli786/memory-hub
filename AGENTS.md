# Second Brain Agent Guide

Treat `raw/` as immutable source material and `wiki/` as the agent-maintained knowledge layer. Before creating or changing a page, search the wiki and inspect `wiki/activity-log.md`. Record material changes with `tools/append_activity.py`; never write operational notes to `wiki/log.md`, which belongs to the ingest process.

Use the wiki page template exactly. Claims need a source reference. Preserve uncertainty and record contradictions instead of resolving them by guesswork. Use `[[wiki-links]]` only for pages that exist or are explicitly proposed.

For codebase questions, build or query `graphify-out/graph.json`; graph results are leads, so open the current source before making a change. The graph pipeline has one designated writer. A separate contributor may commit a completed snapshot, but two writers must never update the same graph artifact concurrently.

The memory layer has L0 source turns, L1 extracted facts, and L2 work-period summaries. Session-start recall is advisory context, never proof. Do not expose identity, authorization, service addresses, or local configuration in a wiki page, prompt, test fixture, log entry, or commit.
