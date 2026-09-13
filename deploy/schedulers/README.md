# Scheduled Jobs

Hooks provide low-latency capture while an agent is active. Schedulers provide
durability: they catch missed sessions, turn approved raw exports into a review
queue, refresh task views, and rebuild the graph from completed knowledge.

## Job ownership

| Job | Suggested cadence | Owner | Safe outcome |
| --- | --- | --- | --- |
| Session sweeper | Every 30 minutes | Client machine | Emit unsent capture batches; never modify a transcript |
| Source intake and queue | Hourly or operator-selected | Vault machine | Collect approved exports and create a review queue |
| Wiki ingest | After reviewed queue approval | One worker | Curate approved pages; never overwrite protected pages |
| Graph refresh | Hourly after wiki work | Designated graph host | Replace one graph snapshot only after a complete build |
| Task publication | Daily | Task owner machine | Regenerate views from the task source of truth |
| Container reconciliation | Scheduled health, explicit apply | Memory host | Rebuild/restart only through controlled apply |
| Container health/backup | Daily health, regular backup | Memory host | Alert or create consistent backup; never silently erase state |

## Rules

- One job must own one mutable artifact at a time. Use a lock for ingest and
  graph writes; a skipped overlapping run is safer than concurrent writers.
- Scheduled shells do not inherit an interactive session. Use absolute binary
  and repository paths in the local, untracked registration—not values copied
  from this repository.
- Each job writes a local log and ends with a named outcome: `SUCCESS`,
  `PARTIAL`, `BLOCKED`, or `FAILED`.
- A scheduler must not retry the same non-transient error indefinitely.
- Test every job manually, then verify one actual scheduled run before relying
  on it.

See `cron.example`, `launchd.template.plist`, and `windows-task.md`.

The portable scripts are `automation/vault_cycle.py`, `automation/stale_pages.py`,
`automation/graph_refresh.py`, and `automation/container_reconcile.py`. The
first three are safe local maintenance; container reconciliation is plan-only
until an operator passes `--apply` against their private compose file.
