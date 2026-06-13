# ASH-45F Calibration Determinism / Replay Seal

## Status
PASS_ASH_45F_CALIBRATION_DETERMINISM_REPLAY_SEAL

## Sealed
- AshCalibrationDeterministicIdKind
- AshCalibrationHashAlgorithm
- AshCalibrationCanonicalOrderingVersion
- AshCalibrationDeterministicHashSource
- AshCalibrationReplayInputSeal
- AshCalibrationReplayComparisonStatus
- AshCalibrationReplayComparisonReport
- AshCalibrationDeterminismReport
- deterministic calibration id derivation
- deterministic evidence id derivation
- deterministic adjustment id derivation
- deterministic profile id derivation
- deterministic snapshot bundle id derivation
- canonical ordering normalization
- replay input seal
- same-input same-output validation
- output fingerprint preservation

## Policy
- Same input must produce same output.
- Same semantic content must not drift ids.
- Evidence order must not change output.
- Adjustment evidence_ids must be sorted before id derivation.
- Random UUID is forbidden for calibration determinism.
- DefaultHasher is forbidden in calibration_determinism.rs.
- System time must not be read implicitly inside calibration id derivation.
- now_unix_ms must be explicit input.
- Snapshot bundle remains primary SSOT.
- runtime router config is not mutated.
- current pointer is not changed.
- no LoRA attach/detach.
- no Python validator.

## Boundary
ASH-45F only seals deterministic replay.
ASH-46 handles Plasticity Dataset Sanitizer / PromptRef Resolver.
ASH-48 handles explicit runtime apply.
ASH-50 handles online calibration ledger / drift monitor.
