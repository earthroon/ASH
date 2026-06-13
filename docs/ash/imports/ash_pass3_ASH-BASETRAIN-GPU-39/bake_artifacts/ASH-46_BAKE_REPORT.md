# ASH-46 Bake Report

## Commit
ASH-46 — Plasticity Dataset Sanitizer / PromptRef Resolver

## Status
PASS_ASH_46_PLASTICITY_DATASET_MANIFEST

## Added
- crates/ash_core/src/prompt_ref_resolver.rs
- crates/ash_core/src/plasticity_dataset_sanitizer.rs
- crates/orchestrator_local/src/ash_46_plasticity_dataset_sanitizer_report.rs
- crates/orchestrator_local/src/bin/ash_46_plasticity_dataset_sanitizer_audit.rs
- acceptance_reports/ASH-46_plasticity_dataset_sanitizer_prompt_ref_resolver.md
- workspace/event_sft/plasticity/* latest candidate snapshots

## Sealed Behaviors
- prompt_ref resolution trace is required.
- Missing/ambiguous prompt_ref is quarantined/rejected instead of fabricated.
- Eval/Holdout leakage blocks training candidates.
- Label conflicts are detected and not averaged.
- Manual review and pointer mismatch sources are quarantined.
- Sanitized dataset remains candidate-only.

## Explicit Non-Goals
- No SFT/DPO training execution.
- No runtime hot reload.
- No LoRA attach/detach.
- No current pointer mutation.
- No Python validator.
