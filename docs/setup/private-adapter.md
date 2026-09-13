# Private Adapter Contract

The cloneable repository supplies the vault, lifecycle policy, contracts, and local MCP catalog. An operator supplies a private adapter to connect their own coding agent to their own memory and knowledge services.

## Required capabilities

| Capability | Input | Output |
| --- | --- | --- |
| Capture | Accepted batch from `run_capture.py` | Persisted L0 records or explicit failure |
| Recall | Session identity and bounded query | L0/L1/L2 records for `recall_hook.py` |
| Wiki read | Search or page identifier | Current page and freshness state |
| Wiki write | Reviewed page update | Atomic write outcome |
| Graph query | Question or symbol | Snapshot result with generation time |

The adapter owns authorization, user scope, protected configuration, and all service routing. It must make a failed read distinguishable from an empty result, avoid destructive operations by default, and record enough observability to diagnose capture and recall failures.

## Agent connection sequence

1. Clone this repository and complete the local wiki setup.
2. Register Claude hooks or the Codex MCP catalog from the supplied templates.
3. Implement or select a private adapter matching the capability table.
4. Feed recall output into `hooks/recall_hook.py` and capture output from `hooks/run_capture.py` into the adapter.
5. Register read-only memory, wiki, and graph operations through the agent’s local MCP configuration.
6. Test an empty result, denied access, slow dependency, duplicate capture, and service restart before importing personal data.

The resulting agent has the same capability model as this architecture while keeping the operator’s data and connectivity independent.
