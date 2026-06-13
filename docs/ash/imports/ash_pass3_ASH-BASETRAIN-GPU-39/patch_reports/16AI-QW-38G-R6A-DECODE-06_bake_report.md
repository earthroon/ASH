# 16AI-QW-38G-R6A-DECODE-06 Bake Report

## Result

status: PASS_STATIC_CONTROLLED_GUARD_CONTRACT
base: 16AI-QW-38G-R6A-DECODE-05 baked tree

## Added source files

- crates/ash_core/src/transition_guard_policy.rs
- crates/ash_core/src/token_penalty_overlay.rs
- crates/ash_core/src/transition_guard_controlled.rs
- crates/ash_core/src/transition_guard_receipt.rs

## Modified source files

- crates/ash_core/src/enko_decode_quality_receipt.rs
- crates/ash_core/src/enko_decode_quality.rs
- crates/ash_core/src/lib.rs

## Receipt Summary

- guard_receipt_created_count: 4
- allow_decision_count: 1
- hard_block_decision_count: 1
- soft_penalty_decision_count: 1
- step_integrity_skip_count: 1
- blocked_token_count: 1
- penalized_token_count: 1
- fixture_token_scores_mutated_count: 2

## Runtime Seal

- runtime_decode_executed_count: 0
- model_forward_executed_count: 0
- sampling_executed_count: 0
- fixture_guard_executed_count: 4
- production_default_apply: false

## Compile Note

cargo/rustc were not available in this environment, so this bake is sealed as a static controlled guard contract rather than a compiled runtime proof.
