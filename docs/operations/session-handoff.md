# Session Handoff Model

A new session receives a compact continuation packet, not an uncontrolled dump of old context.

| Layer | Purpose in the handoff | Gate |
| --- | --- | --- |
| Reviewed persona | Stable working preferences | Explicit human-reviewed block only |
| L0 | Recent prior conversation tail | Same project, bounded message count, freshness window |
| L1 | Decisions and durable facts | Dated and recent only |
| L2 | Work-period navigation summaries | Dated and recent only |
| Wiki and graph | Deeper evidence | Retrieved on demand, never injected wholesale |

The handoff record must say that it is context, not verified truth. It should point the agent to source material and tell it to verify state that may have changed. Old or undated dynamic material remains searchable but is omitted from automatic injection.

This design preserves continuity without letting a stale summary override current user instructions or the working tree.
