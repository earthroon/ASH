# TCU-14 TensorCube Native Path Preflight / Same-Device Borrow Gate

## Status
PASS_TCU_14_NATIVE_PATH_READY

## Sealed
- AshTensorCubeNativePathPreflightMode
- AshTensorCubeNativePathRequirement
- AshTensorCubeNativePathRequirementStatus
- AshTensorCubeSameDeviceBorrowGateDecision
- AshTensorCubeNativePathPreflightDecision
- AshTensorCubeNativePathBlockerKind
- AshTensorCubeNativePathBlocker
- AshTensorCubeNativePathPreflight
- AshTensorCubeNativePathPreflightReport
- same-device borrow gate
- native path blocker generation
- host fallback degraded candidate path
- TCU-12 bridge integration from native preflight

## Policy
- Native path requires trusted TensorCube telemetry snapshot.
- Missing raw bridge blocks native path.
- Missing runtime splice blocks hot reload native path.
- Missing same-device borrow blocks native path when required.
- CPU materialize blocks native path.
- Promotion failure blocks native path.
- Host fallback creates degraded candidate or blocker according to config.
- Missing telemetry cannot be treated as native ready.
- Preflight is read-only.
- Runtime pointer is not mutated.
- LoRA attach/detach is not executed.
- TensorCube buffer is not mutated.
- SFT/DPO training is not executed.
- No Python validator.

## Boundary
TCU-14 only performs TensorCube native path preflight.
TCU-15 handles host fallback pressure guard.
TCU-16 handles LoRA hot reload buffer lease seal.
TCU-17 handles runtime splice replay determinism.
