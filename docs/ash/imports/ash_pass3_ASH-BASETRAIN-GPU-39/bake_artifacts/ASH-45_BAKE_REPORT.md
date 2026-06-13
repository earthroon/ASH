# ASH-45 Bake Report

## Commit
ASH-45 — Adaptive Event Tag Router Scoring / Online Calibration

## Status
BAKED_STATIC_PASS_RUNTIME_TEST_PENDING

## Added Files

### ash_core
- `crates/ash_core/src/event_tag_router_calibration.rs`
- `crates/ash_core/src/event_tag_scoring_profile.rs`
- `crates/ash_core/src/adapter_activation_calibration.rs`
- `crates/ash_core/src/event_tag_calibration_evidence.rs`
- `crates/ash_core/tests/ash_45_event_tag_router_calibration.rs`
- `crates/ash_core/tests/ash_45_event_tag_scoring_profile.rs`
- `crates/ash_core/tests/ash_45_adapter_activation_calibration.rs`
- `crates/ash_core/tests/ash_45_event_tag_calibration_evidence.rs`

### orchestrator_local
- `crates/orchestrator_local/src/ash_45_event_tag_router_calibration_report.rs`
- `crates/orchestrator_local/src/bin/ash_45_event_tag_router_calibration_audit.rs`
- `crates/orchestrator_local/tests/ash_45_event_tag_router_calibration_report.rs`

### reports / snapshots
- `acceptance_reports/ASH-45_adaptive_event_tag_router_scoring_calibration.md`
- `bake_artifacts/ASH-45_STATIC_AUDIT_RESULT.md`
- `bake_artifacts/ASH-45_BAKE_REPORT.md`
- `workspace/event_sft/calibration/ash_event_tag_router_calibration_report_latest.json`
- `workspace/event_sft/calibration/ash_event_tag_scoring_profile_candidate_latest.json`
- `workspace/event_sft/calibration/ash_adapter_activation_calibration_summary_latest.json`

## Modified Files
- `crates/ash_core/src/lib.rs`
- `crates/orchestrator_local/src/lib.rs`
- `crates/ash_core/src/event_tag_runtime_router.rs`

## Patch Note
`event_tag_runtime_router.rs` had an ASH-44 audit helper call to `build_ash_43_runtime_router_audit_reentry_candidate()` but the helper itself was missing in the SSOT ZIP. ASH-45 bake adds that deterministic evidence-only fixture helper so existing ASH-44 and new ASH-45 audit fixtures have a stable activation-plan seed. This helper does not mutate runtime state.

## Sealed Policy
- Calibration profile remains candidate-only.
- `requires_explicit_apply=true` is enforced.
- `applied=false` is enforced.
- Conflicting evidence is not averaged.
- Runtime router config is not mutated.
- ASH-38 routing policy is not mutated.
- ASH-34 temporal overlay is not mutated.
- Current pointer is not changed.
- Runtime hot reload is not executed.
- LoRA attach/detach is not executed.
- Python validator is not added.

## Validation Commands
```bash
cargo test -p ash_core ash_45_event_tag_router_calibration
cargo test -p ash_core ash_45_event_tag_scoring_profile
cargo test -p ash_core ash_45_adapter_activation_calibration
cargo test -p ash_core ash_45_event_tag_calibration_evidence
cargo test -p orchestrator_local ash_45_event_tag_router_calibration_report
cargo run -p orchestrator_local --bin ash_45_event_tag_router_calibration_audit
```

## Container Validation
Static audit passed. Rust-native execution is pending because `cargo` is unavailable in this container.
