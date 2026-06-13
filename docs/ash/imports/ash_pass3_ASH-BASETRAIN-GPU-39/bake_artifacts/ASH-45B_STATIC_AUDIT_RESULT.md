# ASH-45B Static Audit Result

## Status
PASS_STATIC_AUDIT_ASH_45B

## Checked
- `calibration_safety.rs` exists.
- `AshCalibrationSafetyFlag` exists.
- `AshCalibrationSafetyDecision` exists.
- `AshCalibrationSafetySeal` exists.
- `TelemetryRegression` maps to `ManualReview`, not `IncreaseAffinity`.
- scoring adjustments carry safety seal fields.
- profile/report carry safety counts.
- ASH-45B audit status constant exists.
- no `tools/validate_ash_45b_static.py` was added.

## Runtime compile
Not executed in this environment because `cargo` and `rustc` are unavailable.
