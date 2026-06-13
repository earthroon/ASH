# ASH-15 streaming telemetry header / final orchestrator output merge

## Status
PASS_STATIC / PASS_STREAMING_TELEMETRY_FINAL_OUTPUT_MERGE

## Sealed
- RuntimeAshStreamingEvent
- RuntimeAshStreamingTelemetryHeader
- OrchestratorAshFinalTelemetry
- OrchestratorAshFinalOutput
- runtime output -> orchestrator final output merge
- streaming header validation
- final output telemetry validation

## Telemetry fields
- attached_lora_ids
- missing_lora_ids
- runtime_registry_ready
- base_only_explicit
- silent_fallback_detected
- target_auto_remap_detected
- inference_started
- inference_completed

## Runtime policy
- streaming first event must include telemetry header
- AdapterEnabled final output requires attached_lora_ids
- BaseOnlyExplicit final output allows empty attached_lora_ids
- Rejected runtime output cannot become PASS final output
- streaming header must match final output telemetry

## Guards
- no telemetry field rename
- no attached_lora_ids drop
- no silent fallback hiding
- no target auto-remap hiding
- Python validator forbidden

## Boundary
runtime emits telemetry.
orchestrator_local merges telemetry into final output.
ash_core does not execute or format inference output.
