# 16AI-QW-38G-R6A-DECODE-17 Bake Report

## Cue Boundary Decode Contract / Subtitle Timing-Aware Output Seal

status: PASS_STATIC_CUE_BOUNDARY_CONTRACT
base: 16AI-QW-38G-R6A-DECODE-16
domain_ssot: en_to_ko_translation_subtitle_machine

## Added Rust modules

- crates/ash_core/src/cue_boundary_policy.rs
- crates/ash_core/src/cue_timing_snapshot.rs
- crates/ash_core/src/subtitle_timing_budget.rs
- crates/ash_core/src/candidate_timing_fit.rs
- crates/ash_core/src/cue_boundary_violation.rs
- crates/ash_core/src/cue_boundary_contract.rs
- crates/ash_core/src/cue_boundary_contract_receipt.rs
- crates/ash_core/src/cue_boundary_stub.rs

## Static contract result

- cue_boundary_receipt_created_count: 7
- deterministic_key_created_count: 7
- pass_cue_boundary_contract_count: 1
- review_required_count: 3
- compression_recommended_count: 2
- retry_decode_recommended_count: 1
- duplicate_receipt_key_count: 0

## Non-execution guarantees

- candidate_reject_executed_count: 0
- compression_executed_count: 0
- line_reflow_executed_count: 0
- retry_decode_executed_count: 0
- rollback_executed_count: 0
- model_forward_executed_count: 0
- sampling_executed_count: 0
- subtitle_export_executed_count: 0

## Note

This patch seals timing-aware cue boundary output fitness only. It does not compress, reflow, retry, export, or mutate candidates.
