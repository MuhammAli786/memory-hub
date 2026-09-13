# TencentDB Agent Memory Setup

This architecture uses the upstream MIT-licensed TencentDB Agent Memory project as a Git submodule at `vendor/TencentDB-Agent-Memory`.

```sh
git clone --recurse-submodules <this-repository>
```

If the repository was already cloned:

```sh
git submodule update --init --recursive
```

The upstream project supplies the three service implementations this architecture builds around:

| Upstream component | Role here |
| --- | --- |
| MemoryCore | Conversation capture and L0/L1/L2/L3 memory lifecycle |
| MemoryKnowledge | Wiki and code-graph persistence and retrieval |
| MemoryPanel | Optional browser-based operational panel |

Follow the upstream project’s installation instructions for supported images and version-specific settings. Then follow this repository’s [container guide](../../deploy/containers/README.md) to separate persistent memory and knowledge data, [embedding guide](../operations/embeddings.md), and [private-adapter contract](private-adapter.md) to connect agents.

Pin the submodule revision for a deployment and update it through a tested upgrade branch. The upstream project evolves independently; do not treat a newer upstream revision as automatically compatible with existing memory data.
