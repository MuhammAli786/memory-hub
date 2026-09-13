---
description: Audit local and private wiki consistency without changing either
---

# LintDB

Read-only audit. First check private-store readiness; stop if it is unavailable
instead of interpreting an empty page list as an empty wiki.

Report separately: local/private divergence, pages missing on either side,
invalid/missing frontmatter, broken links, index omissions, stale pages, graph
freshness, and contradictions. Name each affected page and evidence. Do not
repair, sync, delete, or overwrite during this command; recommend the smallest
safe next operation instead.
