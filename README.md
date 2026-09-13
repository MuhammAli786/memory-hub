# Memory Hub

A private-by-default, cloneable operating system for an agent-assisted knowledge
vault. It combines TencentDB Agent Memory, a sourced wiki, session memory,
Graphify/code graphs, local or hosted model lanes, an optional panel, and
scheduled maintenance—without committing personal data, credentials, hosts, or
live routing configuration.

## Repository structure

```text
bootstrap/       empty-state templates and migration checklist
raw/             immutable user-owned source intake
wiki/            sourced pages, index, templates, activity log
projects/        reusable operating documents
hooks/           capture, recall, sweep, and persona utilities
tools/           intake, queue, wiki, graph, and model-router tools
automation/      stale-page, graph, container, and vault-cycle maintenance
mcp/             local progressive-discovery catalog
skills/          detailed agent workflows
.claude/commands/ database-backed procedures only
deploy/           containers, router, and scheduler templates
vendor/           TencentDB Agent Memory upstream submodule
```

## System flow

```text
approved exports → raw/ → queue → model/human curation → wiki
agent sessions → hooks → L0 → L1 facts + L2 scenes → bounded handoff
approved wiki + code/conversations → one graph writer → Graphify MCP
memory-core + knowledge + embeddings + optional panel → private agent adapter
```

Hooks capture memory; they do not automatically create wiki pages. Wiki content
is created only through reviewed ingestion with source provenance.

The running deployment is multi-machine: coding-agent clients and a local
Graphify MCP connect through a private tailnet to an always-on memory/knowledge
host, which may use separate trusted accelerator hosts through the tiered model
router. Read the [system integration map](docs/operations/system-integrations.md)
and [Tailnet deployment boundary](deploy/tailnet/README.md) before configuring
your own network.

## How it works

```mermaid
flowchart TD
    A[User-owned exports and notes] --> B[Raw source intake]
    B --> C{Quality and dedupe gate}
    C -->|Approved| D[Review queue]
    C -->|Thin duplicate or excluded| E[Deferred with reason]
    D --> F[Local or approved hosted model]
    F --> G[Human and deterministic verification]
    G --> H[Curated wiki and activity log]

    I[Coding-agent session] --> J[Capture hooks]
    J --> K[L0 conversation records]
    K --> L[L1 facts and L2 work scenes]
    L --> M[Fresh reviewed session handoff]
    M --> I

    H --> N[Single-writer graph refresh]
    K --> N
    N --> O[Graphify MCP and code-graph queries]

    P[Memory core knowledge service embeddings and panel] --> Q[Private agent adapter]
    Q --> I
    L --> P
    H --> P

    R[Scheduled maintenance] --> J
    R --> B
    R --> N
    R --> P
```

## What happens when a user opens a new conversation

```mermaid
flowchart TD
    A[User opens a new Claude, Codex, or compatible agent conversation] --> B[SessionStart event]
    B --> C[Private retrieval adapter validates scope and requests bounded context]
    C --> D{Fresh reviewed context available?}
    D -->|Yes| E[Recall policy filters persona plus recent L0, L1, and L2 records]
    D -->|No or dependency unavailable| F[Return an empty context block and continue]
    E --> G[Agent receives advisory continuation context]
    F --> G
    G --> H[Agent handles the user's current request]
    H --> I{Needs deeper evidence?}
    I -->|Yes| J[Query the private memory adapter, sourced wiki, or Graphify on demand]
    I -->|No| K[Continue with current-session work]
    J --> K
    K --> L[Stop or SessionEnd event]
    L --> M[Capture policy selects substantive transcript turns and deduplicates them]
    M --> N[Private persistence adapter stores accepted turns as L0]
    N --> O[Background extraction may derive L1 facts and L2 work scenes]
    O --> P[Later sessions receive only fresh, bounded, advisory context]
```

The start path is deliberately fail-open: unavailable retrieval never prevents a
new conversation. Conversation capture preserves continuity, but it does not
automatically turn a chat into a wiki page; curation remains a reviewed step.

## Quick start

1. Clone with upstream services: `git clone --recurse-submodules <repository>`.
2. Read [CLAUDE.md](CLAUDE.md), [AGENTS.md](AGENTS.md), and the
   [setup tutorial](docs/setup/tutorial.md).
3. Add only your own exports under `raw/`.
4. Deploy the upstream components with [TencentDB setup](docs/setup/tencentdb-agent-memory.md).
5. Select embeddings and model lanes with [embedding](docs/operations/embeddings.md)
   and [model policy](docs/operations/model-lane.md).
6. Register Claude or Codex using [agent integration](docs/claude-and-codex.md)
   and implement a protected [private adapter](docs/setup/private-adapter.md).
7. Register and test only the needed jobs from [schedulers](deploy/schedulers/README.md).

## Operations

| Need | Procedure or tool |
| --- | --- |
| Collect exports | `/pull-sourcesDB`, `tools/source_intake.py` |
| Triage / curate | `/triageDB`, `/ingestDB`, `tools/ingest_queue.py` |
| Log / audit | `/logDB`, `/lintDB`, `tools/wiki_maintenance.py` |
| Retrieve knowledge | `/queryDB`, Graphify MCP, private memory adapter |
| Maintain state | `automation/stale_pages.py`, `automation/graph_refresh.py` |
| Reconcile services | `automation/container_reconcile.py --apply` |
| Run safe local cycle | `automation/vault_cycle.py` |

## Scheduled maintenance

The reference cron file, launchd template, and Windows Task Scheduler guide are
in [deploy/schedulers](deploy/schedulers/README.md). Register only the jobs
your private deployment needs; the scripts here are portable templates, not
live production registrations.

| Job | Reference cadence | Purpose |
| --- | --- | --- |
| Session sweeper | Every 30 minutes | Captures batches missed by normal stop/end hooks |
| Source intake and queue refresh | Hourly | Collects approved exports and prepares the review queue |
| Wiki ingest | After review approval | Curates approved material without overwriting protected pages |
| Graph refresh | Hourly after intake | Rebuilds the one-writer graph snapshot from completed knowledge |
| Task publication | Daily | Regenerates task views from their source of truth |
| Container health and backup | Daily / regular backup | Checks persistence and creates consistent backups |
| Container reconciliation | Scheduled health check; explicit apply | Plans service convergence; rebuilds or restarts only with `--apply` |

See the concrete reference entries in
[cron.example](deploy/schedulers/cron.example),
[launchd.template.plist](deploy/schedulers/launchd.template.plist), and
[windows-task.md](deploy/schedulers/windows-task.md). Every scheduled run
should produce a local log and a named `SUCCESS`, `PARTIAL`, `BLOCKED`, or
`FAILED` outcome.

## Models, privacy, and private code

Local models suit sensitive embeddings, extraction, summaries, and bounded
classification. Hosted research lanes may handle explicitly approved
non-sensitive research, never private raw sources by default. Models propose;
source evidence and deterministic validation decide durable knowledge.

The reference embedding model is `nomic-embed-text-v1.5` at 768 dimensions.
Changing its identity requires re-embedding all vectors. For private repository
graphs, build beside a trusted checkout or use a dedicated read-only identity
outside Git. See [private code graphs](docs/setup/private-code-graphs.md).

## Publication gate

```sh
python3 -m unittest discover -s tests
python3 tools/audit_release.py .
```

Also run a secret scanner and manual review before changing repository visibility.
