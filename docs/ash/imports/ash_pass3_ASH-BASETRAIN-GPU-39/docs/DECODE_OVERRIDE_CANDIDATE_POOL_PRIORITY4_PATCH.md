# Decode Override Candidate Pool Priority 4 Patch

## Scope
This patch promotes candidate-pool reranking from text-only telemetry scoring to decode-aware scoring.

## Added runtime structures
- `StandardInferCandidatePoolRerankRequest`
- `TelemetryCandidatePoolRerankWeights`
- `TelemetryCandidatePoolRerankScore`
- `TelemetryCandidatePoolRerankDecision`

## Added scoring axes
- structure score
- length adequacy score
- anti-shorts penalty
- telemetry confidence score
- decode stability score
- min-length contract score

## Decode-aware inputs consumed
- `decode_override_snapshot.temperature`
- `decode_override_snapshot.top_p`
- `decode_override_snapshot.top_k`
- `decode_override_snapshot.min_new_tokens`
- `sampled_decode_applied`
- `finish_reason`
- `mean_logprob`
- `min_logprob`

## Entry point
- `run_standard_infer_candidate_pool_reranked(...)`

## Notes
This patch keeps the older `run_standard_infer_reranked(...)` path intact and adds a dedicated candidate-pool decision type so that candidate output metadata is not discarded or forced back into `StandardInferResult`.
