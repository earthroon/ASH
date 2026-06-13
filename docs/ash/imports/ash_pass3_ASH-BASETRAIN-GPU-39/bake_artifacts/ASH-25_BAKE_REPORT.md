# ASH-25 Bake Report

## Status
BAKED_STATIC

## SSOT
Input SSOT: ASH-24 baked tree.
Patch contract: ASH-25 Composite LoRA Artifact Planner.

## Added
- crates/ash_core/src/composite_artifact_manifest.rs
- crates/ash_core/src/composite_artifact_planner.rs
- crates/orchestrator_local/src/ash_25_composite_artifact_plan_report.rs
- crates/orchestrator_local/src/bin/ash_25_composite_artifact_planner_audit.rs
- crates/ash_core/tests/ash_25_composite_artifact_planner.rs
- crates/ash_core/tests/ash_25_composite_artifact_manifest.rs
- crates/orchestrator_local/tests/ash_25_composite_artifact_plan_report.rs
- acceptance_reports/ASH-25_composite_lora_artifact_planner.md

## Modified
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Sealed behavior
- Composite profile to adapter artifact descriptor planning.
- Adapter manifest compatibility validation.
- Base checkpoint and tokenizer hash blocker checks.
- Target module compatibility and module-wise fallback planning.
- Rank/dtype compatibility report without tensor reads.
- Bake operation plan generation without execution.
- Manifest candidate generation with checksum placeholder only.
- RuntimeStackOnlyPlan is non-executable artifact bake.
- Actual safetensors creation is forbidden in ASH-25.

## Validation limitation
cargo/rustc are not available in this execution container, so Rust compilation was not executed here. Static source audit and zip integrity checks were performed.
