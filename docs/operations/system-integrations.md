# Reference System Integrations

This is the sanitized role-based view of the running system. It describes how
the parts work together without exposing a person’s machine names, network
identities, credentials, source accounts, or routes.

## Agent clients

The primary client machine runs Claude Code and Codex against the same vault
contract. Optional coding agents can participate through the same capture and
adapter interfaces. Claude uses session-start, stop, and session-end hooks;
Codex and other tools are swept on a schedule when they do not expose a native
per-turn hook.

Each client has two local MCP surfaces:

- **Memory Hub catalog MCP**: progressive discovery of memory, wiki, code-graph,
  and health vocabulary.
- **Graphify MCP**: relationship, path, neighbourhood, and important-node queries
  across the local vault and selected conversation evidence.

The private agent adapter connects those local tools to the operator’s memory
and knowledge services. It owns identity, authorization, and routing.

## Memory and knowledge host

An always-available machine runs separate containers from the TencentDB Agent
Memory upstream:

| Component | Integration role |
| --- | --- |
| MemoryCore | Stores L0 conversations, derives L1 facts/L2 scenes, and manages reviewed persona context |
| MemoryKnowledge | Stores wiki pages, code-graph registrations, and knowledge retrieval metadata |
| MemoryPanel | Optional operational UI over memory and knowledge state |
| Embedding service | Generates vectors for semantic recall; model identity must stay stable |
| Model router | Gives single-endpoint consumers access to tiered model capacity |

MemoryCore and MemoryKnowledge use separate persistent stores. The panel is
stateless and may be rebuilt, but memory and knowledge data require consistent
backup and restore procedures.

## Model lanes

The system uses a tiered router because ingestion, graph extraction, and memory
workers often accept only one model setting. Lower tier wins; backends rotate
within a tier; a backend is benched after a real transport or status failure.

- **Local lane**: private embeddings, sensitive extraction, short summaries,
  bounded classification, and small fact-check candidates.
- **Research lane**: approved non-sensitive research, parallel exploration, or
  bulk candidate generation. The reference pattern uses OpenRouter only when
  the source material is approved to leave the local privacy boundary.
- **Validation lane**: deterministic source checks and human review decide
  durable claims regardless of which model drafted them.

## Source and wiki integrations

User-owned exports arrive through explicitly configured connectors: agent
transcripts, chat exports, note exports, documents, research material, and
optional consented calendar or mail exports. Intake preserves provenance,
deduplicates, and produces a queue. `/ingestDB` is the only workflow that
turns approved material into wiki pages. The activity log records completed
work, and stale-page automation reports pages needing review without rewriting
them.

## Graph and container maintenance

One graph writer builds the Graphify snapshot from accepted wiki pages, selected
conversation evidence, and code. Private repository graphs stay on a trusted
checkout or use a scoped read-only identity. Schedulers run session sweeps,
intake/queue updates, stale-page reporting, graph refresh, task publication,
container health, and backups. Container reconciliation is explicit and
controlled; a scheduler never silently replaces a running deployment.

See [Tailnet deployment](../../deploy/tailnet/README.md), [scheduler jobs](../../deploy/schedulers/README.md), [model routing](model-router.md), and [private code graphs](../setup/private-code-graphs.md).
