# ASH-37 Bake Report

## Commit
ASH-37 — Event-Weighted LoRA SFT Planner

## SSOT
Source: ASH-36 selective plasticity curriculum baked tree.

## Added
- `crates/ash_core/src/event_weighted_lora_sft_plan.rs`
- `crates/ash_core/src/sft_sample_selection_policy.rs`
- `crates/ash_core/src/sft_loss_weight_policy.rs`
- `crates/ash_core/src/sft_training_manifest_candidate.rs`
- `crates/orchestrator_local/src/ash_37_event_weighted_sft_planning_report.rs`
- `crates/orchestrator_local/src/bin/ash_37_event_weighted_lora_sft_planner_audit.rs`
- ASH-37 ash_core and orchestrator tests
- `acceptance_reports/ASH-37_event_weighted_lora_sft_planner.md`

## Modified
- `crates/ash_core/src/lib.rs`
- `crates/orchestrator_local/src/lib.rs`

## Sealed behavior
- ASH-36 curriculum is converted to adapter-specific SFT target plans.
- Sample selection separates TrainHardNegative / TrainCorrection / TrainPositive / TrainStabilityAnchor / SignalOnly / HoldoutEval / Excluded.
- MetadataOnly samples remain SignalOnly and are not used for training text.
- Loss weights are bounded and clamp warnings are recorded.
- Dataset materialization requirements are planned only.
- Training manifest candidates are planned only.
- JSONL export is not performed.
- SFT execution is not performed.
- LoRA tensors, registries and current pointers are not mutated.

## Runtime validation note
This environment does not provide cargo/rustc/rustfmt, so Rust compile/test execution was not performed here. Static audit and zip integrity checks were performed instead.
