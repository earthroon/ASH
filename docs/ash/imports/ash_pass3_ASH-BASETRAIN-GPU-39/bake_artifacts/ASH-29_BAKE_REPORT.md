# ASH-29 Bake Report

## Status
Baked as source patch over ASH-28 SSOT.

## Added
- `crates/ash_core/src/phase_hint_aging.rs`
- `crates/ash_core/src/phase_hint_quarantine.rs`
- `crates/orchestrator_local/src/ash_29_phase_hint_aging_report.rs`
- `crates/orchestrator_local/src/bin/ash_29_phase_hint_aging_audit.rs`
- `crates/ash_core/tests/ash_29_phase_hint_aging.rs`
- `crates/ash_core/tests/ash_29_phase_hint_quarantine.rs`
- `crates/orchestrator_local/tests/ash_29_phase_hint_aging_report.rs`
- `acceptance_reports/ASH-29_phase_hint_confidence_decay_registry_aging.md`

## Modified
- `crates/ash_core/src/lib.rs`
- `crates/orchestrator_local/src/lib.rs`

## Contract
- Source phase registry is never mutated in-place.
- `phase_rad` is not changed by aging.
- Confidence decays by half-life.
- Amplitude decays slower than confidence.
- Runtime smoke / promotion-ready evidence can preserve confidence partially.
- Hard negative / replay block / weight mismatch evidence accelerates decay.
- Stale hints are quarantined, not deleted.
- BuildCandidateWithQuarantine excludes quarantined hints from active phase-field input.
- No Python validator was added.

## Environment note
`cargo`, `rustc`, and `rustfmt` were not available in this container, so Rust compile/test execution could not be performed here. Static audit and zip integrity checks were performed instead.
