# ASH-39 Bake Report

## Commit
ASH-39 — SFT Outcome Evaluation / Replay Feedback Merge

## SSOT
Source: ASH-38 baked worktree.

## Added
- crates/ash_core/src/sft_outcome_evaluation.rs
- crates/ash_core/src/sft_outcome_replay_merge.rs
- crates/ash_core/src/sft_plasticity_delta.rs
- crates/ash_core/src/plasticity_promotion_evidence.rs
- crates/orchestrator_local/src/ash_39_sft_outcome_evaluation_report.rs
- crates/orchestrator_local/src/bin/ash_39_sft_outcome_evaluation_audit.rs
- crates/ash_core/tests/ash_39_sft_outcome_evaluation.rs
- crates/ash_core/tests/ash_39_sft_outcome_replay_merge.rs
- crates/ash_core/tests/ash_39_sft_plasticity_delta.rs
- crates/ash_core/tests/ash_39_plasticity_promotion_evidence.rs
- crates/orchestrator_local/tests/ash_39_sft_outcome_evaluation_report.rs
- acceptance_reports/ASH-39_sft_outcome_evaluation_replay_feedback_merge.md

## Modified
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Guardrails
- no SFT execution
- no JSONL export
- no adapter registry mutation
- no current pointer mutation
- no runtime router auto-apply
- no hard negative buffer deletion
- holdout samples remain evaluation-only
- promotion evidence requires ASH-40 runtime re-entry gate and rollback snapshot
- no Python validator

## Validation
Static audit and zip integrity only. cargo/rustc/rustfmt are unavailable in this container.
