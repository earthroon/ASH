# ASH-45C Bake Report

## Commit
ASH-45C — SFT Outcome Metric Priority Resolver

## Result
PASS_ASH_45C_SFT_OUTCOME_METRIC_PRIORITY_RESOLVER

## Added
- `crates/ash_core/src/sft_outcome_metric_priority.rs`
- `crates/ash_core/tests/ash_45c_sft_metric_priority.rs`
- `crates/ash_core/tests/ash_45c_metric_order_invariance.rs`
- `crates/ash_core/tests/ash_45c_metric_safety_integration.rs`
- `crates/orchestrator_local/tests/ash_45c_sft_metric_priority_report.rs`
- `acceptance_reports/ASH-45C_sft_outcome_metric_priority_resolver.md`
- `bake_artifacts/ASH-45C_BAKE_REPORT.md`
- `bake_artifacts/ASH-45C_STATIC_AUDIT_RESULT.md`

## Modified
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/src/event_tag_calibration_evidence.rs`
- `crates/ash_core/src/event_tag_router_calibration.rs`
- `crates/ash_core/src/event_tag_scoring_profile.rs`
- `crates/orchestrator_local/src/bin/ash_45_event_tag_router_calibration_audit.rs`

## Sealed Behavior
- SFT outcome delta no longer comes from implicit first metric delta.
- Calibration evidence preserves `resolved_metric_signal`, `resolved_metric_kind`, and `metric_resolution_confidence_multiplier`.
- Report/profile preserve `metric_resolution_count`, `metric_fallback_count`, and `metric_conflict_count`.
- ASH-45B safety seal remains authoritative over positive metric deltas.

## Runtime Boundary
No runtime router mutation, current pointer change, adapter registry mutation, LoRA attach/detach, hot reload, or calibration apply is performed.
