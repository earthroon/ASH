# ASH-26 Bake Report

## Commit
ASH-26 — Composite LoRA Artifact Bake / Promotion Bridge

## Input SSOT
- ash_pass3_ASH-25_composite_lora_artifact_planner_baked.zip

## Added
- crates/ash_core/src/composite_artifact_bake.rs
- crates/ash_core/src/composite_artifact_promotion_bridge.rs
- crates/orchestrator_local/src/ash_26_composite_artifact_bake_report.rs
- crates/orchestrator_local/src/bin/ash_26_composite_artifact_bake_audit.rs
- crates/ash_core/tests/ash_26_composite_artifact_bake.rs
- crates/ash_core/tests/ash_26_composite_artifact_promotion_bridge.rs
- crates/orchestrator_local/tests/ash_26_composite_artifact_bake_report.rs
- acceptance_reports/ASH-26_composite_lora_artifact_bake_promotion_bridge.md

## Modified
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Sealed Guards
- DryRun does not create artifact files.
- RuntimeStackOnlyPlan cannot emit safetensors.
- Rejected plans cannot bake.
- Missing manifest candidate blocks bake when required.
- Missing adapter artifact blocks staged bake.
- Staged bake computes non-placeholder SHA-256 checksums.
- Promotion bridge never changes current pointer.
- Promotion bridge requires runtime smoke test and manual promotion.
- Python validator is forbidden.

## Environment Limitation
Cargo/rustc were not available in the execution container, so Rust tests could not be executed here. Static contract audit and zip integrity checks are provided instead.

## Forbidden
- tools/validate_ash_26_static.py was not added.
