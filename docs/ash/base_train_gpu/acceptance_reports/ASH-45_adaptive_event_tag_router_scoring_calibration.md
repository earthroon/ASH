# ASH-45 Adaptive Event Tag Router Scoring / Online Calibration

## Status
PASS_ADAPTIVE_EVENT_TAG_ROUTER_SCORING_CALIBRATION

## Sealed
- `AshEventTagRouterCalibrationMode`
- `AshEventTagCalibrationEvidenceKind`
- `AshEventTagCalibrationDirection`
- `AshCalibrationConfidenceClass`
- `AshEventTagRouterCalibrationEvidence`
- `AshAdapterActivationCalibrationSummary`
- `AshEventTagScoringAdjustment`
- `AshEventTagRouterScoringProfileCandidate`
- `AshEventTagRouterCalibrationReport`
- activation decision to calibration evidence
- outcome/perf/rollback feedback merge
- scoring adjustment calculation
- calibration profile candidate generation
- conflict detection without averaging

## Policy
- ASH-45 does not mutate runtime router config.
- ASH-45 does not mutate ASH-38 routing policy.
- ASH-45 does not mutate ASH-34 temporal overlay.
- ASH-45 does not change current pointer.
- ASH-45 does not hot reload runtime state.
- ASH-45 does not attach or detach LoRA adapters.
- Calibration candidates require explicit apply.
- `applied` must remain false.
- Conflicts require manual review.
- No Python validator.

## Boundary
`ash_core` computes calibration candidates.
`orchestrator_local` reports calibration evidence.
`artifact_store` may preserve optional calibration snapshots.
ASH-48 may explicitly apply profile later.

## State Ownership
- Status SSOT: `AshEventTagRouterCalibrationReport.status`
- Candidate SSOT: `AshEventTagRouterScoringProfileCandidate`
- Runtime active config: not owned by ASH-45
- Current pointer: not owned by ASH-45
- Policy/overlay: not owned by ASH-45

## Reproducibility Trace
Each evidence/adjustment/candidate preserves:
- calibration/source ids
- activation plan id
- activation decision id
- adapter id
- event tag
- before/after multipliers
- evidence ids
- decision rule reason
- `created_at_unix_ms`

## Rust-native Validation Commands
```bash
cargo test -p ash_core ash_45_event_tag_router_calibration
cargo test -p ash_core ash_45_event_tag_scoring_profile
cargo test -p ash_core ash_45_adapter_activation_calibration
cargo test -p ash_core ash_45_event_tag_calibration_evidence
cargo test -p orchestrator_local ash_45_event_tag_router_calibration_report
cargo run -p orchestrator_local --bin ash_45_event_tag_router_calibration_audit
```

## Environment Note
This bake environment does not include `cargo`, so Rust tests were sealed as files and statically audited here. Run the commands above in the project Rust environment.
