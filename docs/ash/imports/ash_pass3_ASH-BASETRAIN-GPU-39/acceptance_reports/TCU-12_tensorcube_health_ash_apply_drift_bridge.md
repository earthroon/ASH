# TCU-12 TensorCube Health -> ASH Apply/Drift Bridge

## Status
PASS_TCU_12_TENSORCUBE_ASH_APPLY_DRIFT_BRIDGE

## Sealed
- AshTensorCubeHealthBridgeMode
- AshTensorCubeHealthBridgeSourceKind
- AshTensorCubeHealthBridgeSeverity
- AshTensorCubeHealthBridgeSignalKind
- AshTensorCubeHealthBridgeSignal
- AshTensorCubeAshBridgeDecision
- AshTensorCubeApplyBridgeBlocker
- AshTensorCubeRollbackBridgeTrigger
- AshTensorCubeDriftBridgeSignal
- AshTensorCubeHealthBridgeConfig
- AshTensorCubeHealthAshBridgeReport
- TensorCube health to ASH-48 apply blocker bridge
- TensorCube health to ASH-49 rollback/safe-mode trigger bridge
- TensorCube health to ASH-50 drift signal bridge

## Policy
- TensorCube critical health blocks apply.
- Missing raw bridge blocks native apply when required.
- Missing runtime splice blocks hot reload when required.
- Same-device borrow missing blocks hot reload when required.
- Host fallback in strict mode blocks apply.
- Promotion failure blocks apply and can trigger rollback review.
- Missing TensorCube telemetry cannot be treated as healthy.
- Bridge emits candidates only.
- Runtime pointer is not mutated.
- LoRA attach/detach is not executed.
- SFT/DPO training is not executed.
- Python validator is not added.

## Boundary
TCU-12 only bridges TensorCube health into ASH apply/rollback/drift systems.
TCU-13 canonicalizes TensorCube runtime telemetry snapshots.
TCU-18 promotes TensorCube metrics into PerfGuard.
