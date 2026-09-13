# Tailnet Deployment Boundary

The reference deployment joins only trusted operator-controlled machines to a
private encrypted tailnet. It does not publish memory, knowledge, panel, model,
or graph services to a public network.

## Role-based topology

```text
primary client machine
  ├── Claude Code, Codex, optional other coding agents
  ├── session hooks, source intake, local Graphify MCP
  └── private agent adapter
             │ private tailnet
always-on memory host
  ├── MemoryCore container
  ├── MemoryKnowledge container
  ├── optional MemoryPanel
  ├── model-router service
  ├── embedding service
  └── container health and backup jobs
             │ private tailnet
accelerator host
  └── one or more local inference backends
```

## Access policy

- Each machine has one role and receives only the connections required for that
  role. A client can reach the memory services; a public internet client cannot.
- The panel is private to trusted tailnet users and uses the same service
  authorization boundary as memory and knowledge reads.
- Container services bind privately; no broad host or internet binding is
  required for normal operation.
- Model-router backends are reachable only by designated service peers.
- Private repository graph builders run where the checkout already exists or
  use a narrowly scoped read-only service identity.
- Tailnet names, addresses, ACL details, and enrollment material are operator
  secrets. Keep them in protected local deployment documentation, not Git.

## Operational checks

1. Confirm each required peer is reachable over the private network.
2. Verify that an untrusted machine cannot reach memory, knowledge, panel, or
   model services.
3. Verify service authorization separately from network reachability.
4. Check health, a real memory search, a wiki read, and a graph query after a
   host restart.
5. Remove a machine’s tailnet access and rotate service authorization when that
   machine is retired or lost.
