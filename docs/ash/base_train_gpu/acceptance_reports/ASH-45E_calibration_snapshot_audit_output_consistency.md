# ASH-45E Calibration Snapshot / Audit Output Consistency

## Status
PASS_ASH_45E_CALIBRATION_SNAPSHOT_AUDIT_OUTPUT_CONSISTENCY

## Sealed
- AshCalibrationSnapshotKind
- AshCalibrationSnapshotConsistencyStatus
- AshCalibrationSnapshotFileEntry
- AshCalibrationSnapshotCountSeal
- AshCalibrationSnapshotManifest
- AshCalibrationSnapshotBundle
- audit-output-derived snapshot bundle
- report / candidate count validation
- metric resolution count validation
- LoRA lineage count validation
- safety suppression count validation
- latest snapshot derivation path

## Policy
- Snapshot bundle is the primary snapshot SSOT.
- latest JSON files are derived from the bundle.
- report and candidate counts must match.
- metric counts must match evidence traces.
- LoRA lineage counts must match evidence traces.
- safety suppressed counts must match adjustment flags.
- mismatch cannot be silently repaired.
- runtime router config is not mutated.
- current pointer is not changed.
- no LoRA attach/detach.
- no Python validator.

## Boundary
ASH-45E only seals snapshot consistency.
ASH-45F handles deterministic replay and hash/id stability.
ASH-48 handles explicit runtime apply.
