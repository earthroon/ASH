# Decode Override Candidate Pool Priority 3 Patch

## Goal
Attach a full per-candidate decode override snapshot to candidate pool outputs so rerankers and traces can see the exact decode contract that produced each candidate.

## Changes
- Added `StandardInferDecodeSnapshot`.
- Extended `StandardInferCandidateOutput` with:
  - `effective_min_new_tokens`
  - `effective_max_new_tokens`
  - `effective_seed`
  - `decode_override_snapshot`
- `run_standard_infer_candidate_pool(...)` now passes request seed into candidate output mapping so seed truth is sealed per candidate.

## Notes
- This patch seals decode metadata into candidate outputs.
- It does **not** yet make rerank consume decode metadata directly.
- It does **not** yet push stop/min-new-token logic fully into model-core.
