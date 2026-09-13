# Private Migration Checklist

Run this outside the public repository and only with the new user’s own data.

1. Back up the source memory and knowledge databases with their native
   consistent-backup mechanism.
2. Validate database integrity before and after transfer.
3. Import raw sources before curated wiki pages so page provenance resolves.
4. Import wiki, index, and activity log together; preserve append-only history.
5. Import memory layers only after the target embedding model is selected.
6. Re-embed data when the target embedding model differs from the source.
7. Build a fresh graph snapshot rather than copying an unknown-staleness graph.
8. Verify one memory search, one wiki read, one graph query, and one session
   handoff before retiring the source installation.
