# ASH-45B Manual Review / Telemetry Regression Safety Seal

## Status
PASS_ASH_45B_MANUAL_REVIEW_TELEMETRY_REGRESSION_SAFETY_SEAL

## Sealed
- AshCalibrationSafetyFlag
- AshCalibrationSafetyDecision
- AshCalibrationSafetySeal
- manual review positive adjustment suppression
- telemetry regression positive adjustment suppression
- improved-but-unsafe safety flag
- group-level safety seal
- conservative penalty allowance for directly attributed telemetry regression
- report safety counts

## Policy
- Manual review is not success.
- Telemetry regression must never IncreaseAffinity.
- Improved outcome with manual review must not auto-boost.
- Positive adjustment is suppressed when unsafe.
- Global telemetry regression is warning/manual-review only.
- Requires manual review propagates to adjustment.
- `applied` remains false.
- runtime router config is not mutated.
- current pointer is not changed.
- no LoRA attach/detach.
- no Python validator.

## Boundary
ASH-45B only seals unsafe calibration directions.
ASH-45C handles SFT metric priority.
ASH-45D handles LoRA artifact lineage binding.
ASH-45E handles snapshot consistency.
ASH-45F handles deterministic replay.
