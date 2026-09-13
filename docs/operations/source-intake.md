# Raw Source Intake

`raw/` is the controlled intake layer. Users choose and connect their own sources; nothing is collected without an explicit connector and consent.

## Good source categories

| Source | Typical destination | Ingestion treatment |
| --- | --- | --- |
| Claude, Codex, or other coding-agent transcripts | `raw/chat-exports/` | Capture lifecycle plus optional exported archive |
| Chat exports | `raw/chat-exports/` | Split into individual conversations before curation |
| Meeting notes and transcripts | `raw/notes/` | Preserve speaker/source provenance |
| Documents, research notes, and articles | `raw/articles/` | Keep original file and source citation |
| Manual notes | `raw/notes/` | Treat as source material, not established fact |
| Calendar or email exports | connector-specific folder | Use explicit filters, strict deduplication, and consent |

## Pipeline when raw material arrives

1. The connector writes an immutable source file with provenance and a stable identifier.
2. The intake step rejects empty, duplicate, malformed, and excluded items before a model sees them.
3. The ingest workflow routes small, bounded items to an approved model and flags large or ambiguous items for human review or splitting.
4. A model may draft a source summary and candidate pages; deterministic checks preserve exact identifiers and reject unsupported claims.
5. A reviewer accepts, edits, or rejects curated pages. Accepted pages update the wiki index and activity log.
6. The graph pipeline incorporates accepted wiki pages and selected L0 records into the next snapshot.

No source connector belongs in this public repository unless its authentication, data handling, and consent model can be safely reviewed. Use `pull-sourcesDB` as the operating procedure and implement individual connectors privately.
