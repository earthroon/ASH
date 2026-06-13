# ASH-27 Bake Report

## Commit
ASH-27 — Hard Negative Replay Evaluation Loop

## SSOT Input
- ASH-26 baked tree
- ASH-22 hard negative replay buffer types
- ASH-26 composite artifact promotion bridge types

## Implemented Files
- `crates/ash_core/src/hard_negative_replay_eval.rs`
- `crates/ash_core/src/replay_promotion_gate.rs`
- `crates/orchestrator_local/src/ash_27_hard_negative_replay_eval_report.rs`
- `crates/orchestrator_local/src/bin/ash_27_hard_negative_replay_eval_audit.rs`
- `crates/ash_core/tests/ash_27_hard_negative_replay_eval.rs`
- `crates/ash_core/tests/ash_27_replay_promotion_gate.rs`
- `crates/orchestrator_local/tests/ash_27_hard_negative_replay_eval_report.rs`

## Sealed Contracts
- Contract-level hard negative replay evaluation
- Candidate adapter overlap scoring
- Critical/silent fallback promotion block
- Missing attached LoRA weight telemetry failure path
- Runtime replay request planning without execution
- Runtime observed result merge
- Promotion gate evidence generation

## Non-goals Preserved
- No registry mutation
- No current pointer mutation
- No suppression apply
- No rollback auto-execution
- No runtime inference from ash_core
- No Python validator

## Verification Note
The current container does not provide `cargo` or `rustc`, so Rust compile/tests were not executed here. Static file-contract audit and zip integrity checks were performed instead.
