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

This project is a reference artifact, not a deployable service. It intentionally excludes live clients, service bindings, identity values, secret material, and configuration loading.

## Verify before publication

```sh
python3 tools/audit_release.py .
python3 -m unittest discover -s tests
```

The audit rejects common credential markers, deployment-address markers, environment-variable access, and private-path markers. Review its output manually as well; automated scanning is a gate, not proof.

See [the security boundary](docs/security.md), [architecture](docs/architecture.md), [MCP contract](docs/mcp.md), and [lifecycle webhook contract](docs/webhooks.md).
