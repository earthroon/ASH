# TCU-16 TensorCube LoRA Hot Reload Buffer Lease Seal

## Status
PASS_TCU_16_BUFFER_LEASE_PLAN

## Sealed
- AshTensorCubeBufferLeaseMode
- AshTensorCubeBufferLeaseKind
- AshTensorCubeBufferOwnershipKind
- AshTensorCubeBufferLifetimeKind
- AshTensorCubeBufferReleasePolicy
- AshTensorCubeBufferLeaseDecision
- AshTensorCubeBufferLeaseBlockerKind
- AshTensorCubeBufferLeaseBlocker
- AshTensorCubeHotReloadBufferLeaseCandidate
- AshTensorCubeHotReloadBufferLeasePreflight
- AshTensorCubeHotReloadBufferLeasePlan
- AshTensorCubeHotReloadBufferLeaseReceipt
- AshTensorCubeHotReloadBufferLeaseReport
- AshTensorCubeBufferLeaseConfig
- native same-device borrow lease candidate
- host fallback lease plan-only path
- previous attachment rollback retention
- lease ownership / lifetime / release policy seal
- TCU-12 bridge integration

## Policy
- Native lease requires native path ready and same-device borrow ready.
- Host fallback lease is plan-only or manual-review by default.
- CPU materialized buffer cannot be lease-ready by default.
- Promotion failure blocks lease.
- Previous attachment snapshot is required when configured.
- Previous attachment is retained for rollback.
- Unknown ownership / lifetime / release policy blocks lease or requires manual review.
- Lease plan does not mutate runtime pointer.
- Lease receipt does not mutate GPU buffer.
- LoRA attach/detach is not executed.
- TensorCube buffer is not mutated.
- No SFT/DPO training execution.
- No Python validator.

## Boundary
TCU-16 only seals buffer lease ownership/lifetime/release planning.
TCU-17 handles runtime splice replay determinism.
TCU-18 promotes TensorCube metrics into PerfGuard.
TCU-19 handles TensorCube emergency demotion / safe tensor mode.
