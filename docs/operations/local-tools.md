# Local Automation Tools

These tools replace only the reusable, local parts of source pulling and wiki
maintenance. They intentionally do not contact personal mail, calendar, note,
or hosted-model accounts.

```sh
# Copy a user-selected export directory into raw/ and retain a dedupe manifest.
python3 tools/source_intake.py --source <export-directory> --destination raw/chat-exports --manifest local-data/source-manifest.json

# Build a model-independent review queue.
python3 tools/ingest_queue.py --raw raw --output local-data/ingest-queue.json

# Rebuild the index or audit the wiki before a private knowledge-store sync.
python3 tools/wiki_maintenance.py index --wiki wiki
python3 tools/wiki_maintenance.py lint --wiki wiki
```

Use the queue as input to a private model adapter or human review workflow. The
adapter must preserve provenance, reject unsupported claims, and write only
approved pages.
