# Setup Tutorial

This guide creates a working local knowledge base and integration structure. It does not configure a hosted memory service; identity, authorization, and service routing stay in an operator-controlled deployment adapter.

## 1. Start the vault

Clone this repository, review `AGENTS.md`, and keep source exports under `raw/`. Initialize the wiki by retaining `wiki/index.md`, `wiki/activity-log.md`, and the provided folders. Add current work to `priorities.md`.

Initialize the upstream TencentDB Agent Memory implementation with the [submodule guide](tencentdb-agent-memory.md), then follow the container guide to run its memory, knowledge, and optional panel components on a dedicated machine.

## 2. Use the wiki

Create one atomic page from `wiki/templates/page.md`. Cite the source under `raw/`, use wiki links for related pages, update `wiki/index.md`, then append a factual entry to the activity log:

```sh
python3 tools/append_activity.py --log wiki/activity-log.md --message "Created a sourced project page."
```

The log is append-only. If a deployment maintains a second database copy, its private adapter must complete the database write before changing the disk copy.

## 3. Register session hooks

Copy `.claude/settings.template.json` into your local Claude settings and replace only the repository-root placeholder. The stop and end hooks call `hooks/run_capture.py`; it emits an offline batch and cannot send data anywhere. Wire a private adapter to persist those batches only after it has been separately audited.

For Codex, use `.codex/config.template.toml` as the local MCP registration template. The bundled MCP catalog is read-only and configuration-free.

## 4. Add recall safely

Use `hooks/recall_hook.py` as the policy layer. Give it reviewed L0, L1, and L2 JSON through standard input. It filters undated or old dynamic material and emits `additionalContext`. A private retrieval adapter is responsible for obtaining those records.

## 5. Build the code graph

Run the local structural baseline:

```sh
python3 tools/build_code_graph.py --root . --output graphify-out/graph.json
```

For richer document and relationship extraction, install Graphify separately and use its documented local pipeline. Designate one writer for `graphify-out/graph.json`; treat graph output as a navigation aid and verify relevant source files before acting.

For a private repository, use the [private code-graph guide](private-code-graphs.md). Build locally beside an existing checkout by default; only let a knowledge service clone the repository with a dedicated read-only identity held outside version control.

## 6. Add a memory backend

Choose a memory backend and write a private adapter that maps accepted capture batches to L0, extraction output to L1, and scene summaries to L2. Keep all connection data, identity values, authorisation material, and persistence endpoints in the deployment’s protected configuration system—not in this repository.

Choose a local, hosted, or routed model for extraction and review work. Follow [the model-lane policy](../operations/model-lane.md) and [tiered router guide](../operations/model-router.md): models may propose and classify, but source evidence and deterministic checks decide what becomes durable knowledge.

## 7. Register scheduled jobs

Use the [scheduler guide](../../deploy/schedulers/README.md) after the manual
workflow works. Register the session sweeper, source intake, graph refresh,
task publication, and backup jobs locally with only the capabilities that user
has actually configured. Test each one manually and verify a real scheduled run.
