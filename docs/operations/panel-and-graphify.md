# Panel UI and Graphify MCP

## Panel UI

The optional upstream MemoryPanel is a stateless operational interface over the memory and knowledge services. It can expose memory layers, wiki pages, graph inventory, and operational status. Keep it read-only for generated task or activity views unless there is a single authoritative writer; a second writer silently creates conflicting state.

Build the panel from the upstream `MemoryPanel` component only after its memory and knowledge dependencies are healthy. Do not bake operator configuration or secret material into the image. Verify every expected route after an update; a successful build does not prove that a dashboard view remains present.

## Graphify MCP

Graphify builds a relationship graph over code, wiki pages, and selected conversation material. Its MCP surface lets a coding agent query relationships, neighbourhoods, paths, and graph-wide important nodes.

Use Graphify when an agent needs to answer how components relate, trace callers, understand a project’s structure, or traverse across wiki and conversation evidence. It complements the TencentDB code graph: the TencentDB graph indexes registered repositories, while Graphify can combine local vault material and conversation context into one relationship graph.

Store graph snapshots under `graphify-out/`, designate one writer, and expose Graphify to an agent through a local standard-input MCP registration. Query results are starting points; read the current source before relying on a relation.

For a private code repository, keep the Graphify process on a trusted machine
with the checkout, or provision a dedicated read-only service identity outside
version control. See [private repository code graphs](../setup/private-code-graphs.md).
