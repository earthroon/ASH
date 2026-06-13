# 16AI-QW-32 Static Validation Result

## Result

STATIC_VALIDATION: PASS
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE

## Checks

- module exists: True
- test file exists: True
- lib.rs export exists: True
- required symbols missing: []
- test function count: 51
- brace balance: True (153 open / 153 close)
- acceptance report exists: True
- bake report exists: True

## Required symbol set

- QWaveRuntimeCanaryApplyCandidateReceipt
- QWaveRuntimeCanaryApplyGateRef
- QWaveRuntimeCanaryRollbackDisableRef
- QWaveRuntimeCanaryFeatureFlagDryRunPlan
- QWaveRuntimeCanaryTelemetryPreflightPlan
- QWaveRuntimeCanaryPercentageClampReport
- QWaveRuntimeCanarySafetyReadinessReport
- QWaveRuntimeCanaryApplyCandidateEntry
- QWaveRuntimeCanaryApplyEligibilityReport
- QWaveRuntimeCanaryApplyReviewStatus
- QWaveRuntimeCanaryApplyScope
- QWaveRuntimeCanaryApplyNextStage
- AcceptedCanaryApplyCandidate
- RejectedMissingQw30RuntimeApplyGateReceipt
- RejectedApplyGateSourceInvalid
- RejectedMissingQw31RollbackDisableReceipt
- RejectedRollbackDisableNotReady
- RejectedMissingFeatureFlagDryRunPlan
- RejectedSilentEnableAllowed
- RejectedAutoEnableAllowed
- RejectedCanaryPercentageZero
- RejectedCanaryPercentageOutOfBounds
- RejectedSafetyReadinessFailed
- RejectedActualFeatureFlagEnable
- RejectedRuntimeEnable
- RejectedCanaryApplyExecution
