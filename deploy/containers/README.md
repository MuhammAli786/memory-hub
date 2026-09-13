# Container Hosting Tutorial

Run the memory and knowledge services as separate containers on a dedicated always-available machine. They may share one container engine, but they must have separate persistent volumes and independent health checks.

```text
coding-agent clients
        │
        ├── private client adapter
        │
dedicated memory host
  ├── memory-core container     → L0, L1, L2, persona and extraction state
  ├── knowledge container       → wiki pages and code-graph metadata
  ├── embedding service         → vector generation
  └── optional panel            → read-only operational UI
```

## Why separate containers

Memory and knowledge have distinct storage, lifecycle, and failure modes. A memory failure should not rewrite wiki files. A knowledge ingest failure should not prevent session capture. Never run more than one replica against the same SQLite volume.

## Setup sequence

1. Provision a dedicated machine with a supported container runtime and persistent storage.
2. Obtain compatible memory-core and knowledge service source images from their maintainers. This repository intentionally provides no proprietary service source or image reference.
3. Create one persistent volume for memory state and one for knowledge state. Back up each database with its native consistent-backup mechanism; do not copy a live write-ahead-log database file blindly.
4. Build and start `memory-core`; wait for its health check to pass.
5. Build and start `knowledge`; configure it to use the memory service only through a private operator-managed connection.
6. Start an embedding service before enabling semantic recall. Confirm a real embedding response and dimension count before importing data.
7. Connect each coding agent with its own private adapter. Keep identities, authorization material, and routing configuration in protected deployment configuration, never in this Git repository.
8. Verify persistence across a container restart and restore drill before moving any real data.

## Deployment boundary

`deploy/compose.topology.yaml` is deliberately a topology only. It has no addresses, secrets, configuration substitution, or host binding. An operator must create the compatible deployment manifest privately.
