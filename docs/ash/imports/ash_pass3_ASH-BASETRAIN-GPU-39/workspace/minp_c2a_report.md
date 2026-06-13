# 16AI-QW-38G-R6A-MINP-C2A Report

## Scope
Semantic Score Provider Build / Snapshot Alignment Smoke Seal.

## Implemented
- Added `model_core::minp_c2a_snapshot_alignment`.
- Added `SemanticScoreSnapshotAlignmentReport` and alignment status enums.
- Added validator for vocab size, token-id indexability, finite/range checks, optional tokenizer/lm_head alignment, and fixture predicates.
- Added CPU/GPU score buffer alignment receipt structure.
- Added runtime semantic prior gate requiring both:
  - `ASH_SAMPLER04_PROMOTION_STATUS=STRICT_CANDIDATE_READY`
  - `ASH_MINP_C2A_ALIGNMENT_STATUS=PASS`

## Non-scope
- No dynamic QWave/Delta-K scoring.
- No weighted Min-P formula change.
- No shader formula change.
- No semantic prior default enable.

## Execution
`cargo`, `rustc`, `rustfmt`, and runtime vocab manifest were unavailable in this environment. Runtime alignment is therefore recorded as `NOT_RUN`, not `PASS`.
