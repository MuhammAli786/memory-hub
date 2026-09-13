---
description: Audit wiki and private knowledge-store consistency without changing either
---

Read only. Compare the local wiki against the private adapter’s page inventory if available. Report content divergence, pages missing from either store, invalid frontmatter, broken links, or stale graph snapshots separately. If the private wiki is not ready, report that state and stop rather than treating an empty result as an empty knowledge base.
