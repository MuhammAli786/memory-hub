# Second Brain Vault Contract

This repository separates immutable source material from curated knowledge and transient memory.

```text
raw/             source exports and notes; never rewrite them
wiki/            agent-maintained, sourced knowledge pages
journal/         daily working notes
content/         outlines, drafts, and published writing
priorities.md    current user-maintained priorities
hooks/           session lifecycle policy and offline capture utilities
tools/           activity logging and local graph construction
deploy/          container topology and deployment tutorials
skills/          portable agent workflows
```

## Wiki rules

Every page uses the frontmatter fields in `wiki/templates/page.md`. Keep one concept, entity, person, project, comparison, or source summary per page. Attribute claims to source material, use `[[wiki-links]]`, preserve exact names and numbers, and record contradictions explicitly. Update `wiki/index.md` whenever a page is added, renamed, or retired.

`wiki/activity-log.md` is append-only. `wiki/log.md` belongs to the ingest engine and is never a place for vault knowledge.

## Memory rules

L0 is source conversation turns; L1 is extracted facts and decisions; L2 is a narrative summary of a period of work. Session-start context is advisory. Use it to find sources, not as proof. A retrieval adapter must scope and authenticate every read and write outside this repository.

## Model rules

Local, hosted, and routed models may extract, summarize, label, and propose fact checks. They never become the source of truth: validate claims against supplied evidence, preserve exact identifiers, and omit missing information. Changing the embedding model requires regenerating all stored vectors; equal vector dimensions do not establish compatibility.

## Agent rules

Read `priorities.md` and the activity log before a daily briefing or debrief. Search existing wiki pages before creating another. Reject empty input before a model sees it. When information is absent, omit it or ask; never invent an identifier, date, source, or technical detail.

Use the command procedures in `.claude/commands/` and the reusable workflows in `skills/`. For Codex, `AGENTS.md` is the equivalent working contract.
