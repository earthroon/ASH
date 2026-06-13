# ASH-24 Bake Report

## Status
BAKED_STATIC

## SSOT
Input archive: ASH-23 runtime ensemble weight telemetry baked zip.

## Files added
- crates/ash_core/src/phase_hint_registry.rs
- crates/ash_core/src/delta_k_phase_projection.rs
- crates/ash_core/tests/ash_24_phase_hint_registry.rs
- crates/ash_core/tests/ash_24_delta_k_phase_projection.rs
- crates/orchestrator_local/src/ash_24_phase_hint_registry_report.rs
- crates/orchestrator_local/src/bin/ash_24_phase_hint_registry_audit.rs
- crates/orchestrator_local/tests/ash_24_phase_hint_registry_report.rs
- acceptance_reports/ASH-24_learned_phase_hint_registry_delta_k_projection.md
- bake_artifacts/ASH-24_BAKE_REPORT.md
- bake_artifacts/ASH-24_STATIC_AUDIT_RESULT.md

## Files modified
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Sealed behavior
- Learned phase hint registry exists as a separate SSOT from adapter registry.
- Delta-K projection helpers map Delta-K to -pi..pi phase values.
- Circular phase mean is used rather than naive scalar averaging.
- Coactivation ledger events can become phase evidence.
- Hard negative replay cases become repulsion / anti-coherence evidence.
- ASH-23 weight telemetry can become amplitude evidence through a cycle-safe ash_core input mirror.
- Candidate phase registry is built without mutating the previous registry.
- Phase hint registry can be converted into ASH-20 AshPhaseFieldSynapseInput.

## Not executed
cargo/rustc were not available in the container, so Rust compilation/tests were not run here.
