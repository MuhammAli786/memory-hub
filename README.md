# Second Brain Memory Architecture

A security-sanitized reference implementation for a personal knowledge and memory layer. It documents the design, contracts, lifecycle hooks, and a small MCP tool-catalog pattern without including operational data, deployment addresses, user identifiers, credentials, private repositories, or environment-based configuration.

## What this repository contains

```text
contracts/      Versioned JSON shapes for lifecycle events and read-only tools
deploy/         Service-topology reference with no bindings or configuration values
docs/           Architecture, operating model, security boundary, and webhook guide
hooks/          Configuration-free transcript parsing and idempotency utilities
mcp/            Progressive MCP tool discovery implementation and tests
tools/          Offline audit script used before publishing
tests/          Tests for the hook utilities
```

## How it works

1. A session host emits a lifecycle payload through standard input.
2. The capture utility keeps only substantive user/assistant text pairs and gives each pair two deterministic identities.
3. A caller-owned adapter may send accepted records to a memory service. That adapter is intentionally not included: transport, identity, and authorization are deployment concerns.
4. A session-start adapter may retrieve L0 conversation history, L1 facts, and L2 scene summaries, then inject only fresh, explicitly approved context.
5. The MCP server exposes one code-execution tool over a curated, read-only catalog. `search` and `describe` keep full schemas out of every initial model prompt.

This repository now includes the complete reusable vault skeleton: `raw/`, `wiki/`, `journal/`, `content/`, priorities, client instructions, hook templates, a local MCP catalog, and a deterministic code-graph baseline. It intentionally excludes only the live clients, service bindings, identity values, secret material, and deployment configuration.

## Verify before publication

```sh
python3 tools/audit_release.py .
python3 -m unittest discover -s tests
```

The audit rejects common credential markers, deployment-address markers, environment-variable access, and private-path markers. Review its output manually as well; automated scanning is a gate, not proof.

Start with the [setup tutorial](docs/setup/tutorial.md). See the [wiki structure](wiki/README.md), [Claude and Codex integration](docs/claude-and-codex.md), [code-graph pipeline](docs/code-graph.md), [security boundary](docs/security.md), [MCP contract](docs/mcp.md), and [lifecycle webhook contract](docs/webhooks.md).
