# ASH-49 Emergency Rollback / Runtime Safe Mode

## Status
PASS_ASH_49_EMERGENCY_ROLLBACK_PLAN

## Sealed
- AshRuntimeEmergencyRollbackMode
- AshRuntimeEmergencyRollbackTriggerKind
- AshRuntimeEmergencyRollbackTrigger
- AshRuntimeEmergencyRollbackDecision
- AshRuntimeEmergencyRollbackBlockerKind
- AshRuntimeEmergencyRollbackBlocker
- AshRuntimeEmergencyRollbackCandidate
- AshRuntimeEmergencyRollbackPreflight
- AshRuntimeEmergencyRollbackPlan
- AshRuntimeEmergencyRollbackReceipt
- AshRuntimeSafeModeKind
- AshRuntimeSafeModeRestrictionKind
- AshRuntimeSafeModeRestriction
- AshRuntimeSafeModePlan
- AshRuntimeSafeModeReceipt
- AshRuntimeEmergencyRollbackGateReport
- failed apply rollback trigger detection
- previous attachment restoration candidate
- safe mode restriction plan
- rollback receipt / safe mode receipt

## Policy
- Previous attachment snapshot is required for rollback
- Failed apply cannot silently fallback
- Critical perf regression enters safe mode
- Telemetry regression can enter quarantine safe mode
- Safe mode blocks hot reload and pointer mutation
- Rollback target cannot equal failed target
- Rollback plan does not mutate runtime pointer
- rollback_applied=true requires receipt
- current pointer mismatch cannot be auto-corrected
- no SFT/DPO training execution
- no Python validator

## Boundary
ASH-49 defines emergency rollback and runtime safe mode.
ASH-50 handles online calibration ledger / drift monitor.
