# practo-healthcare-support-agent
Final Capstone — Practo Domain Support Agent (CrewAI)
## Task 4: Grounded Generation and Calibration

Embedding model: sentence-transformers/all-MiniLM-L6-v2

Distance metric: Cosine distance

Similarity conversion:
similarity = 1 - cosine_distance

Calibration queries:
- Five in-scope policy queries
- Three deliberately out-of-scope queries

### Fixed-size chunking

- Maximum out-of-scope similarity: [0.06138235330581665]
- Minimum in-scope similarity: [ 0.6114689111709595]
- Selected threshold: [0.33642563223838806]
- Calibration passed: [true]

### Sentence-based chunking

- Maximum out-of-scope similarity: [0.06463193893432617]
- Minimum in-scope similarity: [0.6204134821891785]
- Selected threshold: [0.3425227105617523]
- Calibration passed: [true]

Thresholds are derived from measured score ranges,
not selected from an arbitrary preset.

## Task 5: Chunking Evaluation

Both strategies were evaluated using the same five
in-scope queries, the same embedding model, and top-k = 5.

| Strategy | Mean Precision | Mean Recall |
|---|---:|---:|
| Fixed-size with overlap | 0.25666666666666665 | 1.0 |
| Sentence-based | 0.24666666666666667 |  1.0 |

Per-query results and retrieved document IDs are
available in evaluation/reports/.

### Recommendation

[I would deploy the fixed-size with overlap chunking strategy because it achieved a mean precision of 0.257 and a mean recall of 1.00, compared with 0.247 precision and 1.00 recall for sentence-based chunking. Both strategies retrieved all expected relevant policy documents, but fixed-size chunking achieved slightly higher precision, meaning it returned fewer irrelevant results while maintaining perfect recall in this evaluation. I would validate these results using additional unseen queries before deploying the selected strategy in production.]