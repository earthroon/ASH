# ASH-31 Bake Report

## Commit
ASH-31 — Composite Rank Compression / SVD Bake Experiment

## Source SSOT
ASH-30 baked zip / worktree.

## Files Added
- crates/ash_core/src/composite_rank_compression.rs
- crates/ash_core/src/composite_svd_compression.rs
- crates/ash_core/src/compressed_artifact_bridge.rs
- crates/orchestrator_local/src/ash_31_composite_rank_compression_report.rs
- crates/orchestrator_local/src/bin/ash_31_composite_rank_compression_audit.rs
- crates/ash_core/tests/ash_31_composite_rank_compression.rs
- crates/ash_core/tests/ash_31_composite_svd_compression.rs
- crates/ash_core/tests/ash_31_compressed_artifact_bridge.rs
- crates/orchestrator_local/tests/ash_31_composite_rank_compression_report.rs
- acceptance_reports/ASH-31_composite_rank_compression_svd_experiment.md

## Files Modified
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Sealed Behavior
- Source artifact overwrite is forbidden.
- Current pointer mutation is forbidden.
- Compressed bridge requires runtime smoke, manual review, and current pointer gate.
- Rank 0 compression is rejected.
- Reconstruction error threshold is explicit.
- High-error modules can be kept original only by config.
- Python validator is forbidden.

## Validation
Static audit only in this environment; cargo/rustc are unavailable in container.
