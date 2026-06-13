# ASH-34 Event-Driven LoRA Activation / Temporal Penalty Overlay

## Status
PASS_EVENT_DRIVEN_LORA_ACTIVATION_TEMPORAL_PENALTY

## Sealed
- AshLoraRuntimeEventKind
- AshLoraRuntimeEventSource
- AshTemporalPenaltyTargetKind
- AshTemporalPenaltyCategory
- AshTemporalPenaltyDecayPolicy
- AshLoraRuntimeEvent
- AshRuntimeLoraEventLedger
- AshTemporalPenaltyRecord
- AshTemporalPenaltyOverlay
- AshTemporalSuppressionState
- AshEventDrivenRouteAdjustmentReport
- AshEventDrivenSoftEnsembleAdjustmentReport
- AshLoraCooldownLedger
- event to temporal penalty conversion
- TTL / half-life / cooldown decay
- path action adjustment
- soft ensemble weight suppression
- runtime event bridge

## Policy
- Temporal penalties are short-term overlays.
- Adapter registry is not mutated.
- Current pointer is not changed.
- LoRA tensors are not changed.
- Expired penalties do not affect route/ensemble.
- Original ASH-17 route is preserved.
- Original ASH-19 ensemble is preserved.
- Weight suppression is traceable through source_event_ids.
- No SFT samples are created in ASH-34.
- No Python validator.

## Boundary
ash_core computes event-driven penalty overlays.
runtime emits event telemetry.
orchestrator_local reports adjustment evidence.
artifact_store preserves optional overlay snapshots.
