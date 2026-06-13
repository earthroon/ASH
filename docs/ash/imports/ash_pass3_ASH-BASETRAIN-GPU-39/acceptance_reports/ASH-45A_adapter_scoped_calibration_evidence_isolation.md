# ASH-45A Adapter-Scoped Calibration Evidence Isolation

## Status
PASS_ASH_45A_ADAPTER_SCOPED_CALIBRATION_EVIDENCE_ISOLATION

## Sealed
- AshCalibrationAttributionClass
- AshCalibrationAttributionTrace
- AshCalibrationAttributionDecision
- adapter-scoped rollback attribution
- adapter-scoped perf attribution
- manual review attribution trace
- attribution confidence multiplier
- global warning only path
- unattributed signal adjustment block
- ASH-45 calibration evidence attribution fields
- ASH-45 report attribution counts
- ASH-45A orchestrator audit booleans

## Policy
- Global rollback count must not penalize unrelated adapters.
- Global perf pressure must not mark all adapters regressed.
- Manual review must not become an automatic affinity boost.
- GlobalUnattributed evidence cannot be strong-confidence.
- Unknown attribution cannot auto-adjust unless it is routed to ManualReview.
- Runtime router config is not mutated.
- ASH-38 routing policy is not mutated.
- ASH-34 temporal overlay is not mutated.
- Current pointer is not changed.
- No LoRA attach/detach is executed.
- No hot reload is executed.
- No Python validator is added.

## Boundary
ASH-45A only isolates evidence attribution.
ASH-45B handles manual review / telemetry regression safety.
ASH-45C handles SFT metric priority.
ASH-45D handles LoRA artifact lineage binding.
ASH-45E handles calibration snapshot / audit output consistency.
ASH-45F handles calibration determinism / replay seal.

## Added Files
- crates/ash_core/src/calibration_attribution.rs
- crates/ash_core/tests/ash_45a_calibration_attribution.rs
- crates/ash_core/tests/ash_45a_adapter_scoped_calibration_evidence.rs
- crates/orchestrator_local/tests/ash_45a_adapter_scoped_calibration_report.rs

## Modified Files
- crates/ash_core/src/lib.rs
- crates/ash_core/src/event_tag_calibration_evidence.rs
- crates/ash_core/src/event_tag_router_calibration.rs
- crates/ash_core/src/event_tag_scoring_profile.rs
- crates/ash_core/tests/ash_45_event_tag_calibration_evidence.rs
- crates/ash_core/tests/ash_45_adapter_activation_calibration.rs
- crates/orchestrator_local/src/bin/ash_45_event_tag_router_calibration_audit.rs
- crates/orchestrator_local/tests/ash_45_event_tag_router_calibration_report.rs

## Expected Rust-native Commands
```bash
cargo test -p ash_core ash_45a_calibration_attribution
cargo test -p ash_core ash_45a_adapter_scoped_calibration_evidence
cargo test -p orchestrator_local ash_45a_adapter_scoped_calibration_report
cargo run -p orchestrator_local --bin ash_45_event_tag_router_calibration_audit
```
