# Embedding Model and Semantic Recall

The current architecture used `nomic-embed-text-v1.5` through a compatible embedding server.

| Property | Value |
| --- | --- |
| Model | `nomic-embed-text-v1.5` |
| Vector dimensions | 768 |
| Model input context | 2,048 tokens |
| Conservative source chunk limit | 3,000 characters |
| Retrieval strategy | Hybrid keyword and vector search |

Model identity matters more than dimensionality. Replacing the model with another 768-dimensional model changes the vector space and invalidates comparisons with existing vectors even though no schema error occurs. Re-embed the corpus whenever the embedding model changes.

Before enabling semantic recall, verify that one sample produces 768 dimensions and that the vector is accepted by the memory store. Preserve the exact model name in deployment documentation and migration records.
