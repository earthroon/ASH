# ASH-41 Bake Report

## Commit
ASH-41 — Plasticity Dataset Export / JSONL Materializer

## Source SSOT
ASH-40 baked archive.

## Added
- crates/ash_core/src/plasticity_dataset_export.rs
- crates/ash_core/src/plasticity_jsonl_materializer.rs
- crates/ash_core/src/plasticity_dataset_manifest.rs
- crates/orchestrator_local/src/ash_41_plasticity_dataset_export_report.rs
- crates/orchestrator_local/src/bin/ash_41_plasticity_dataset_export_audit.rs
- crates/ash_core/tests/ash_41_plasticity_dataset_export.rs
- crates/ash_core/tests/ash_41_plasticity_jsonl_materializer.rs
- crates/ash_core/tests/ash_41_plasticity_dataset_manifest.rs
- crates/orchestrator_local/tests/ash_41_plasticity_dataset_export_report.rs
- acceptance_reports/ASH-41_plasticity_dataset_export_jsonl_materializer.md
- bake_artifacts/ASH-41_STATIC_AUDIT_RESULT.md

## Modified
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Sealed Rules
- JSONL materialization only; SFT execution is not allowed.
- MetadataOnly and SignalOnly samples cannot become training text.
- Holdout samples cannot enter train split.
- Missing prompt/output text is rejected; text is not fabricated.
- Dataset artifacts keep requires_explicit_training=true and training_started=false.
- Dataset/manifest checksums are required before training readiness.
- No Python validator was added.

## Verification Boundary
cargo/rustc/rustfmt are unavailable in this container, so Rust compile/tests were not executed here.
Static audit and zip integrity were performed instead.
