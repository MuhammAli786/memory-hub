# Code Graph Pipeline

The graph is a second retrieval layer over the wiki, conversation corpus, and implementation source. It complements search: a search finds text, while a graph exposes relationships and blast radius.

```text
authoritative corpus → normalize → chunk → structural and semantic extraction
→ merge and resolve identifiers → label communities → graph snapshot → query tools
```

## Invariants

- One designated process writes the graph snapshot.
- Fragment checks validate only fragment-local facts; edge resolution happens after merge.
- A graph records `generated_at` and source inventory. Freshness is never inferred from a generic status field.
- Automated extraction may propose edges; it must not invent source identifiers.
- Queries return leads, not a substitute for reading the current file.

`tools/build_code_graph.py` is the dependency-free baseline. It emits functions, imports, and call-name edges from Python files. A full Graphify deployment can extend this with more languages and document relationships.

For private repositories, follow the [private code-graph guide](setup/private-code-graphs.md). The recommended default is to build beside an existing private checkout; a knowledge-service clone needs its own least-privilege read identity managed outside Git.
