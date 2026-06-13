# ASH-47 HardNegative Preference Dataset / DPO Bridge

## Status
PASS_ASH_47_DPO_BRIDGE_MANIFEST

## Sealed
- AshPreferenceDatasetBuildMode
- AshPreferencePairKind
- AshPreferencePairDecision
- AshPreferencePairIssueKind
- AshPreferencePairIssueSeverity
- AshPreferencePairIssue
- AshHardNegativePreferencePair
- AshDpoBridgeSample
- AshHardNegativePreferenceDatasetCandidate
- AshDpoBridgeManifest
- AshHardNegativePreferenceDatasetReport
- hard-negative preference pairing
- DPO bridge sample generation
- pair polarity validation
- duplicate and mirror pair detection
- prompt lineage validation
- adapter/event tag validation
- source trace preservation

## Policy
- HardNegative cannot become chosen side
- TelemetryRegression cannot become chosen side
- chosen and rejected must not be identical
- prompt lineage mismatch rejects pair
- adapter/event tag mismatch rejects pair by default
- manual review required sample cannot auto-enter DPO bridge
- eval/holdout leakage blocks pair
- mirror pair is rejected or manual review
- DPO bridge is candidate only
- No DPO/SFT training execution
- runtime router config is not mutated
- current pointer is not changed
- no LoRA attach/detach
- no Python validator

## Boundary
ASH-47 only builds preference dataset candidates and DPO bridge samples.
ASH-48 handles Runtime LoRA Hot Reload / Explicit Apply Gate.
ASH-50 handles online calibration ledger / drift monitor.
