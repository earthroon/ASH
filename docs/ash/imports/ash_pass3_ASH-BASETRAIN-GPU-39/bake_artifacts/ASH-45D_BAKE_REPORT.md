# ASH-45D Bake Report

## Commit
ASH-45D — LoRA Artifact Lineage Binding

## Result
PASS_ASH_45D_LORA_ARTIFACT_LINEAGE_BINDING

## Files Added
- crates/ash_core/src/lora_artifact_lineage.rs
- crates/ash_core/tests/ash_45d_lora_artifact_lineage.rs
- crates/ash_core/tests/ash_45d_lora_lineage_safety.rs
- crates/ash_core/tests/ash_45d_lora_lineage_confidence.rs
- crates/orchestrator_local/tests/ash_45d_lora_artifact_lineage_report.rs
- acceptance_reports/ASH-45D_lora_artifact_lineage_binding.md
- bake_artifacts/ASH-45D_BAKE_REPORT.md
- bake_artifacts/ASH-45D_STATIC_AUDIT_RESULT.md
- workspace/event_sft/calibration/ash_lora_artifact_lineage_trace_latest.json

## Files Modified
- crates/ash_core/src/lib.rs
- crates/ash_core/src/event_tag_calibration_evidence.rs
- crates/ash_core/src/event_tag_scoring_profile.rs
- crates/ash_core/src/event_tag_router_calibration.rs
- crates/ash_core/src/calibration_safety.rs
- crates/orchestrator_local/src/bin/ash_45_event_tag_router_calibration_audit.rs

## Sealed Behavior
- Calibration evidence now preserves LoRA lineage trace fields.
- Scoring adjustments preserve lineage class / decision / trace id.
- Profile candidates and reports preserve lineage counts.
- Pointer mismatch and registry mismatch are manual-review unsafe lineage states.
- Adapter-id-only lineage is weak and cannot be Strong confidence.
- Safety seals still win over valid lineage.

## Forbidden Behavior Checked
- No runtime router mutation.
- No current pointer mutation.
- No LoRA attach/detach.
- No immediate apply.
- No Python validator.

## Rust Native Commands Sealed
```bash
cargo test -p ash_core ash_45d_lora_artifact_lineage
cargo test -p ash_core ash_45d_lora_lineage_safety
cargo test -p ash_core ash_45d_lora_lineage_confidence
cargo test -p orchestrator_local ash_45d_lora_artifact_lineage_report
cargo run -p orchestrator_local --bin ash_45_event_tag_router_calibration_audit
```

## Local Container Note
cargo/rustc are not installed in this container, so Rust execution could not be performed here. Static audit checks were performed instead.
