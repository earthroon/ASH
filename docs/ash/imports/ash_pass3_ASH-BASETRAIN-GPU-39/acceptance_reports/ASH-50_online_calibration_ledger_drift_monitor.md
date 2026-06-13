# ASH-50 Online Calibration Ledger / Drift Monitor

## Status
PASS_ASH_50_RUNTIME_DRIFT_MONITOR

## Sealed
- AshOnlineCalibrationLedgerEventKind
- AshOnlineCalibrationLedgerEntry
- AshOnlineCalibrationLedgerCorrectionEntry
- AshOnlineCalibrationLedgerSnapshot
- AshRuntimeDriftSignalKind
- AshRuntimeDriftSignalSeverity
- AshRuntimeDriftSignal
- AshRuntimeDriftWindow
- AshRuntimeDriftMonitorConfig
- AshRuntimeDriftRecommendationKind
- AshRuntimeDriftRecommendation
- AshOnlineCalibrationDriftReport
- append-only ledger chain
- apply / rollback / safe-mode event extraction
- drift signal detection
- drift recommendation candidate generation

## Policy
- Ledger is append-only
- Existing entries are never mutated
- Corrections are new entries
- Sequence numbers must be monotonic
- Previous entry hash must match
- Drift report does not mutate runtime state
- Recommendations are candidates only
- runtime router config is not mutated
- current pointer is not changed
- no LoRA attach/detach
- no SFT/DPO training execution
- no Python validator

## Boundary
ASH-50 records and monitors online calibration/runtime drift.
Future ASH-51+ may consume drift recommendations for policy update gates.
