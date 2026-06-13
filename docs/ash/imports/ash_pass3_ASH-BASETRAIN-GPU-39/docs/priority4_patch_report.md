# Priority 4 Patch Report

## What changed
- runtime reranker now consumes decode override snapshot fields directly
- candidate pool rerank decision path added
- decode stability and min-length contract scoring added
- tie-break now prefers structure, telemetry confidence, sampled application, then lower anti-shorts penalty

## New exported API
- `run_standard_infer_candidate_pool_reranked(...)`
- `StandardInferCandidatePoolRerankRequest`
- `TelemetryCandidatePoolRerankDecision`
- `TelemetryCandidatePoolRerankWeights`

## Limits
- task-specific candidate diversity policy is not included yet
- stop/min-new-token model-core ownership is still deferred to next stage
- compile verification not performed in this environment
