# Model Lane and Verification Policy

The vault is model-agnostic. A local model, a hosted model, or a routed pool of models may perform extraction, drafting, classification, graph labeling, or candidate fact checks. The model is a worker, not an authority.

## Assign work by risk

| Task | A local or hosted model may do it | Required guardrail |
| --- | --- | --- |
| Extract candidate L1 facts | Yes | Omit unsupported fields; retain source links |
| Draft L2 scenes | Yes | Mark as summary; bound recency and source scope |
| Ingest a raw document | Yes | Reject empty input; preserve exact identifiers; review claims |
| Classify intake or graph edges | Yes | Validate output against known files and source text |
| Propose related wiki pages | Yes | Treat empty result as valid; require evidence before writing links |
| Fact check a claim | Yes | Compare against supplied primary source; do not accept model confidence as evidence |
| Change priorities, publish, delete, or resolve a contradiction | No autonomous authority | Human or deterministic policy decision required |

## Local and hosted deployment choices

A local model keeps source material within the operator’s infrastructure and is useful for private bulk work. A hosted model may provide more capacity or quality but requires an explicit data-handling decision. A router can select among models, but callers must still check response shape, errors, and output completeness.

Prompts and schemas must state that missing information is omitted, never guessed. For identifiers, dates, versions, names, and quantities, copy exact source text. When the model is given truncated input, label it partial and prohibit completion by assumption.

## Fact-checking workflow

1. Give the model the exact claim and bounded source material.
2. Require a structured verdict: supported, contradicted, insufficient evidence, or source unavailable.
3. Require exact supporting excerpts or source locations for supported and contradicted results.
4. Validate quoted identifiers and links mechanically where possible.
5. Do not write a claim to the wiki unless the evidence itself supports it.

## Embeddings are different

An embedding model is part of the data format. The current reference uses `nomic-embed-text-v1.5` at 768 dimensions. Another model can replace it, whether local or hosted, but all existing vectors must be regenerated with the replacement. Matching dimensions alone is not compatibility.
