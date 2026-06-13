# ASH-28 Runtime Composite Attachment Smoke Gate

## Status
PASS_RUNTIME_COMPOSITE_ATTACHMENT_SMOKE_GATE

## Sealed
- AshRuntimeCompositeSmokeMode
- AshRuntimeCompositeSmokeDecision
- AshRuntimeCompositeSmokeSeverity
- AshRuntimeCompositeSmokeTarget
- AshRuntimeCompositeSmokeConfig
- AshRuntimeCompositeSmokeObservedTelemetry
- AshRuntimeCompositeSmokeRequest
- AshRuntimeCompositeSmokeReport
- AshCompositePromotionReadyEvidence
- promotion bridge to smoke target conversion
- dry-run smoke validation
- observed telemetry merge
- attached_lora_ids validation
- attached_lora_weights validation
- composite profile / artifact / promotion bridge trace validation
- ASH-27 replay eval block integration
- promotion-ready evidence generation

## Policy
- ASH-28 does not change current pointer.
- ASH-28 does not promote artifacts automatically.
- ASH-28 does not rollback automatically.
- Runtime smoke requires ASH-23 attached_lora_weights telemetry.
- Silent fallback is fail-hard.
- Missing streaming header is fail-hard.
- Missing final output is fail-hard.
- Replay-blocked candidates cannot pass smoke.
- Ready evidence still requires manual promotion and current pointer gate.
- No Python validator.

## Boundary
ash_core defines smoke gate contracts.
runtime emits observed smoke telemetry.
orchestrator_local merges and reports smoke evidence.
artifact_store preserves smoke snapshots.
