# 16AI-QW-38G-R6A-DECODE-11 Bake Report

## Summary

Baked DECODE-11 on top of DECODE-10. Added a degeneration-risk final gate that consumes surface rerank output and candidate risk receipts, rejects unsafe selected candidates, selects safe fallback candidates inside the existing pool, or routes unsafe pools to review.

## Added modules

- crates/ash_core/src/degeneration_risk_policy.rs
- crates/ash_core/src/degeneration_risk_snapshot.rs
- crates/ash_core/src/salad_aware_final_gate.rs
- crates/ash_core/src/fallback_candidate_selection.rs
- crates/ash_core/src/salad_aware_final_gate_receipt.rs

## Modified modules

- crates/ash_core/src/enko_decode_quality_receipt.rs
- crates/ash_core/src/lib.rs

## Static status

status: PASS_STATIC_DEGENERATION_RISK_FINAL_GATE_CONTRACT
runtime_decode_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0
qe_model_executed_count: 0
source_adequacy_executed_count: 0
glossary_constraint_executed_count: 0

## Note

Rust compilation was not executed in this environment. This bake is a static contract/fixture/report seal.
