# Model Router and Tiering

Some consumers accept only one model configuration. A router gives them one stable internal model lane while selecting among multiple backends.

## Tier rule

Lower `tier` wins. Within the same tier, the router rotates the starting backend for each request. List order is not priority; it is only the initial rotation order.

```text
tier 0: local backends — round-robin for capacity and privacy
tier 1: approved research backends — round-robin if they share quota
tier 2: optional emergency capacity
```

The router filters out backends whose context window cannot fit the estimated prompt plus requested output. On transport or status failure it benches that backend briefly and tries the next candidate. It does not declare a slow or low-quality answer failed: quality validation belongs to the caller, and latency policy must be explicit.

`tools/model_router.py` is a dependency-free, configuration-file selection core. `tools/model_router_server.py` is the matching proxy runtime. Neither contains endpoint or credential values. The operator creates an untracked local copy of the backend config, provides its own private backend URLs and optional credential-file paths, and starts the server with explicit bind and port arguments. Use the selector to test order:

```sh
python3 tools/model_router.py --config deploy/router/backends.template.json --estimated-tokens 2000
```

## Workload policy

- Use local models for private embeddings, sensitive source extraction, small summaries, and bounded classification where local capacity is suitable.
- Use an explicitly approved hosted research lane for non-sensitive parallel research, broad literature exploration, or bulk candidate generation. One operator pattern is to use OpenRouter’s research models because independent instances can run concurrently with little or no paid usage when eligible models are selected.
- Do not send private transcripts, personal notes, or unreviewed raw vault content to a hosted model merely because it is convenient.
- Make the request’s output budget fit the same context window as prompt, tool schemas, and response format. A visible short answer can still need substantial hidden reasoning budget on some models.
- Local or hosted fact-check models return candidate verdicts only. Verify against source evidence before durable writes.
