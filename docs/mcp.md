# MCP Design

The MCP aggregation layer exposes a single sandboxed `code` operation. Inside the sandbox, each approved upstream operation appears as `codemode.<name>(input)`.

The initial description names only `search` and `describe` plus the available operation names. A caller discovers relevant tools first, requests signatures for the selected names, and then performs the query. This reduces context overhead and avoids asking a model to invent argument names.

## Curated operation groups

| Group | Purpose | Allowed in this reference |
| --- | --- | --- |
| L0 | Search original conversation turns | Yes, read-only |
| L1 | Search extracted facts | Yes, read-only |
| L2 | List and read work-period summaries | Yes, read-only |
| Wiki | Search and read curated knowledge | Yes, read-only |
| Code graph | Inspect symbols, callers, and freshness | Yes, read-only |
| Administration | Delete, overwrite, publish, ingest | No |

The schema examples are intentionally opaque: callers supply identity and authorization through an external, reviewed integration layer.
