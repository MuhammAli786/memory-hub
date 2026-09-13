# Component Coverage

This table records the implementation families represented by the reference repository and the deliberate publication boundary for each.

| Component | Reference included | Operational code excluded |
| --- | --- | --- |
| Session capture | Transcript parser, two-key identity, tail-window selection, fail-open runner | Persistence adapter and deployment-specific routing |
| Session recall | Input and output contract, freshness rule, approval requirement | Retrieval client and identity selection |
| Periodic sweep | Lifecycle semantics and idempotency model | Host scheduler registration and local state locations |
| Persona control | Protected manual-content rule | Read and write client |
| MCP code mode | Progressive `search` and `describe` catalog | Upstream connections and sandbox launcher |
| Knowledge and memory services | Container topology and ownership boundaries | Build sources, bindings, data volumes, and runtime configuration |
| Model tool harness | Failure-exit principles: done, blocked, repeated-error stop | Model provider client and local execution details |
| Panel | Its stateless role over memory and knowledge | Panel registry and all service connections |

The omissions are intentional. A public reference may explain interfaces and safety invariants, but it must not bundle a path to a live personal system.
