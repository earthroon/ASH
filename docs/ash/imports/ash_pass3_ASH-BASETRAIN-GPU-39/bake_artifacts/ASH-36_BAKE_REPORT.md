# ASH-36 Bake Report

## SSOT
Source zip/worktree: ASH-35 Event-to-SFT Sample Ledger baked state.

## Added
- crates/ash_core/src/selective_plasticity_curriculum.rs
- crates/ash_core/src/curriculum_bucket_builder.rs
- crates/ash_core/src/adapter_training_intent.rs
- crates/orchestrator_local/src/ash_36_selective_plasticity_curriculum_report.rs
- crates/orchestrator_local/src/bin/ash_36_selective_plasticity_curriculum_audit.rs
- crates/ash_core/tests/ash_36_selective_plasticity_curriculum.rs
- crates/ash_core/tests/ash_36_curriculum_bucket_builder.rs
- crates/ash_core/tests/ash_36_adapter_training_intent.rs
- crates/orchestrator_local/tests/ash_36_selective_plasticity_curriculum_report.rs
- acceptance_reports/ASH-36_selective_plasticity_curriculum_builder.md

## Modified
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Sealed Behavior
- ASH-35 sample ledger is converted to selective plasticity curriculum buckets.
- HardNegative / Correction / Positive / MetadataSignal / Excluded roles are separated.
- MetadataOnly samples remain signal-only and are not exportable text.
- Adapter training intent plans aggregate bucket/sample weight evidence.
- Source sample ledger is not mutated.
- JSONL export and SFT execution are not implemented in ASH-36.

## Runtime Boundary
ASH-36 does not call runtime inference, mutate current pointers, mutate adapter registries, or alter LoRA tensors.
