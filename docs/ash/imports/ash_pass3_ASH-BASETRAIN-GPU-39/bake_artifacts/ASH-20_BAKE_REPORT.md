# ASH-20 Bake Report

## Commit
ASH-20 — Phase-Field Synapse Penalty / Imaginary Action Experiment

## SSOT
Input SSOT: ASH-19 baked tree.

## Added files
- `crates/ash_core/src/phase_field_synapse.rs`
- `crates/ash_core/tests/ash_20_phase_field_synapse.rs`
- `crates/orchestrator_local/src/ash_20_phase_field_report.rs`
- `crates/orchestrator_local/src/bin/ash_20_phase_field_synapse_audit.rs`
- `crates/orchestrator_local/tests/ash_20_phase_field_report.rs`
- `acceptance_reports/ASH-20_phase_field_synapse_penalty_imaginary_action.md`
- `bake_artifacts/ASH-20_BAKE_REPORT.md`
- `bake_artifacts/ASH-20_STATIC_AUDIT_RESULT.md`

## Modified files
- `crates/ash_core/src/lib.rs`
- `crates/orchestrator_local/src/lib.rs`

## Sealed behavior
- Phase hints are accepted as explicit experimental input.
- `ReportOnly` computes phase terms but does not change selected path/adapters.
- `AdjustRoute` uses `real_action_after = real_action_before + phase_penalty` for route adjustment.
- `imaginary_action` is recorded as trace only and is not used as complex probability.
- Missing phase hints warn or reject by config.
- Base-only routes bypass phase adjustment.
- No registry mutation.
- No tensor mutation.
- No Python validator.

## Verification limitation
The current container does not expose `cargo`, `rustc`, or `rustfmt`, so Rust compilation could not be executed here. Static file audit and package integrity checks were performed instead.
