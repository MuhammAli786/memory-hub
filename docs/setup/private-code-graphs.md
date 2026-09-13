# Private Repository Code Graphs

Private source code can be indexed without making the repository public. Choose
one of two deployment patterns.

## Pattern A: trusted local graph builder

Run Graphify or the structural graph builder on a machine that already has a
normal private checkout and permission to read it.

```text
private checkout → local graph build → reviewed graph snapshot → private knowledge adapter
```

This is the simplest option. The graph builder uses the operator’s existing
repository access; the memory or knowledge containers never clone source code.
Use this when source must remain on a developer machine or a dedicated build
worker.

## Pattern B: read-only knowledge-service clone

Give the knowledge service a dedicated read-only repository identity through
the operator’s secret-management system. Use a deploy key, repository-scoped
machine identity, or equivalent least-privilege credential that can read only
the selected repository.

```text
private repository → read-only service identity → knowledge-service clone → code graph
```

Mount or inject that identity only at runtime. Never put it in a compose file,
image layer, source-controlled configuration file, command history, graph
artifact, or log. Rotate it independently and remove it when a repository is
no longer indexed.

## Required registration fields

The private adapter needs a repository display name, immutable repository
identifier, selected branch or revision, source classification, and graph
ownership. It must record the resolved revision and graph generation time.
Do not interpret a generic `ready` state as proof that the graph reflects the
current branch.

## Security and freshness checks

1. Confirm the service can read the exact requested revision.
2. Confirm the identity cannot write, administer, or access unrelated repos.
3. Confirm clone failures surface as failures rather than an empty graph.
4. Keep graph artifacts in the same privacy boundary as source code.
5. Rebuild after a meaningful revision change; record the revision in metadata.
6. Query the graph only as a lead, then read current source before acting.

## Graphify MCP

For private repos, run Graphify locally beside the checkout and register its
standard-input MCP server with the coding agent. The agent can then query
symbols, neighbours, paths, and relationships without uploading the source to a
third-party service. If semantic extraction uses a hosted model, make a separate
explicit data-handling decision first; structural extraction does not require it.
