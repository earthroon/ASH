# ASH-30 Bake Report

## SSOT
Input SSOT: ash_pass3_ASH-29_phase_hint_confidence_decay_registry_aging_baked.zip

## Added
- crates/ash_core/src/composite_artifact_registry.rs
- crates/ash_core/src/composite_current_pointer.rs
- crates/ash_core/src/composite_pointer_lineage.rs
- crates/orchestrator_local/src/ash_30_composite_artifact_registry_report.rs
- crates/orchestrator_local/src/bin/ash_30_composite_artifact_registry_audit.rs
- crates/ash_core/tests/ash_30_composite_artifact_registry.rs
- crates/ash_core/tests/ash_30_composite_current_pointer.rs
- crates/ash_core/tests/ash_30_composite_pointer_lineage.rs
- crates/orchestrator_local/tests/ash_30_composite_artifact_registry_report.rs
- acceptance_reports/ASH-30_composite_artifact_registry_current_pointer.md

## Modified
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Sealed Behavior
- Artifact registry registration and current pointer activation are separate.
- DryRun never mutates registry/current pointer.
- RegisterCandidate registers a candidate record without changing current pointer.
- RegisterAndPromoteToCurrent requires previous stable pointer by default.
- Promotion-ready evidence, smoke pass evidence, replay pass evidence, checksum presence, and attached LoRA weight availability are enforced before current pointer candidate creation.
- Replay-blocked evidence rejects current promotion.
- Previous current pointer is preserved as previous stable snapshot.
- Pointer lineage records MovedToPreviousStable and PromotedToCurrent events.

## Runtime Note
cargo/rustc/rustfmt were not available in this container, so Rust compilation was not executed here. Static audit and zip integrity checks were performed instead.
