# ASH-42 Bake Report

## Source SSOT
- Base zip: ASH-41 plasticity dataset export / JSONL materializer bake
- Commit: ASH-42 Event-Weighted LoRA SFT Executor / Training Run Gate

## Added
- crates/ash_core/src/sft_training_run_gate.rs
- crates/ash_core/src/sft_training_command_plan.rs
- crates/ash_core/src/trained_lora_adapter_artifact.rs
- crates/ash_core/src/sft_training_result_report.rs
- crates/orchestrator_local/src/ash_42_sft_training_run_report.rs
- crates/orchestrator_local/src/bin/ash_42_event_weighted_lora_sft_executor_audit.rs
- crates/ash_core/tests/ash_42_sft_training_run_gate.rs
- crates/ash_core/tests/ash_42_sft_training_command_plan.rs
- crates/ash_core/tests/ash_42_trained_lora_adapter_artifact.rs
- crates/ash_core/tests/ash_42_sft_training_result_report.rs
- crates/orchestrator_local/tests/ash_42_sft_training_run_report.rs
- acceptance_reports/ASH-42_event_weighted_lora_sft_executor.md
- bake_artifacts/ASH-42_BAKE_REPORT.md
- bake_artifacts/ASH-42_STATIC_AUDIT_RESULT.md

## Modified
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Sealed Behavior
- Dataset artifact and training manifest validation
- Explicit training gate
- Command plan generation
- Training telemetry contract
- Trained LoRA adapter artifact capture
- Training result report
- Backend execution boundary remains orchestrator_local only

## Negative Guarantees
- No adapter registry mutation
- No current pointer change
- No runtime router auto-apply
- No JSONL materialization in ASH-42
- No Python validator
