# Claude and Codex Integration

Both clients use the same vault contract, but their registration files differ.

## Claude

`.claude/settings.template.json` defines three hooks:

| Event | Script | Result |
| --- | --- | --- |
| SessionStart | `hooks/recall_hook.py` | Injects only reviewed and fresh supplied context |
| Stop | `hooks/run_capture.py` | Emits selected transcript turns |
| SessionEnd | `hooks/run_capture.py` | Emits a final selected batch |

The host passes a lifecycle envelope on standard input. The included scripts do not make a connection. A private adapter may consume their JSON output.

The eight DB command files provide source intake, ingest, logging, querying,
briefing, debrief, lint, and triage procedures so the client uses one private
knowledge-aware operating surface.

Copy `.claude/mcp.template.json` into the agent’s private MCP registration and replace the repository-root placeholder. Build the local catalog first. Install Graphify locally before registering its graph MCP entry; it indexes the cloned vault and does not need the operator’s memory-service configuration.

## Codex

`AGENTS.md` is the project instruction contract. `.codex/config.template.toml` registers the local MCP catalog. After building `mcp/`, Codex can call the catalog’s `search` and `describe` operations to discover the L0, L1, L2, wiki, and code-graph vocabulary before talking to a separately configured private backend.

The same template registers Graphify as a second local MCP server. It supports relationship queries across the vault and complements TencentDB’s registered-repository code graph.

## Shared rule

Neither integration template contains a personal identity, secret, address, protocol endpoint, or environment setting. Local deployment configuration belongs outside the repository and must be reviewed before it can persist or retrieve user data.
