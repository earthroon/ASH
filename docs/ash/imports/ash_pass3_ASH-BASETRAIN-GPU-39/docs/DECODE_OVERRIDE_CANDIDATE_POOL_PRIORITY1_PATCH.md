# Decode Override Candidate Pool Priority 1 Patch

## Goal
Establish `StandardInferDecodeOverride` as the decode-override SSOT for candidate generation.

## Included
- `StandardInferDecodeOverride`
- `StandardInferCandidatePlan`
- `StandardInferCandidateOutput`
- `run_standard_infer_candidate_pool(...)`

## Current behavior
- candidate generation freezes the original request context and varies only per-candidate request fields that are currently supported by `StandardInferRequest` (`seed`, `max_new_tokens`)
- override metadata (`temperature`, `top_p`, `top_k`, `stop_sequences`) is preserved in candidate outputs as the single decode-override snapshot
- sampled decode application still depends on lower layers; this patch only establishes the runtime contract

## Not yet included
- infer core applying `temperature/top_p/top_k/stop_sequences` directly from `StandardInferDecodeOverride`
- reranker consuming the override snapshot
- task-profile driven override planning
