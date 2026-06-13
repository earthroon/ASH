# ASH-45C Static Audit Result

## Status
PASS_STATIC_AUDIT_ASH_45C

## Checks
- PASS_SFT_OUTCOME_METRIC_PRIORITY_MODULE_PRESENT
- PASS_LIB_EXPORT_PRESENT
- PASS_NO_IMPLICIT_FIRST_DELTA_SCAN
- PASS_EVIDENCE_METRIC_TRACE_FIELDS_PRESENT
- PASS_PROFILE_METRIC_COUNT_FIELDS_PRESENT
- PASS_AUDIT_REPORT_ASH_45C_STATUS_PRESENT
- PASS_NO_PYTHON_VALIDATOR_45C

## Rust-native commands sealed but not executed in this environment
```bash
cargo test -p ash_core ash_45c_sft_metric_priority
cargo test -p ash_core ash_45c_metric_order_invariance
cargo test -p ash_core ash_45c_metric_safety_integration
cargo test -p orchestrator_local ash_45c_sft_metric_priority_report
cargo run -p orchestrator_local --bin ash_45_event_tag_router_calibration_audit
```
