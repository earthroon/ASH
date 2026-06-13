# TCU-15 TensorCube Host Fallback Pressure Guard

## Status
PASS_TCU_15_FALLBACK_PRESSURE_WARNING

## Sealed
- AshTensorCubeFallbackPressureMode
- AshTensorCubeFallbackPressureFactorKind
- AshTensorCubeFallbackPressureSeverity
- AshTensorCubeFallbackPressureFactor
- AshTensorCubeFallbackPressureScore
- AshTensorCubeFallbackPressureDecision
- AshTensorCubeFallbackPressureGuard
- AshTensorCubeFallbackPressureGuardReport
- AshTensorCubeFallbackPressureGuardConfig
- fallback pressure scoring
- host fallback accumulation detection
- CPU materialize blocker path
- promotion failure critical / rollback-review path
- TCU-12 bridge integration from fallback pressure guard

## Policy
- Host fallback is tracked as pressure, not ignored.
- Repeated host fallback can emit drift signal.
- CPU materialize blocks native apply when configured.
- Promotion failure blocks native path and may trigger rollback review.
- Fallback pressure does not mutate runtime state.
- Runtime pointer is not mutated.
- LoRA attach/detach is not executed.
- TensorCube buffer is not mutated.
- Host fallback is not directly executed.
- CPU materialize is not directly executed.
- SFT/DPO training is not executed.
- No Python validator.

## Boundary
TCU-15 only computes fallback pressure guard.
TCU-16 handles LoRA hot reload buffer lease seal.
TCU-17 handles runtime splice replay determinism.
TCU-18 promotes TensorCube metrics into PerfGuard.
