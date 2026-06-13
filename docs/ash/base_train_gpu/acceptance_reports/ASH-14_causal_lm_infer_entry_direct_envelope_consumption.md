# ASH-14 causal_lm / infer_entry direct envelope consumption

## Status
PASS_STATIC / PASS_CAUSAL_LM_INFER_ENTRY_ASH_ENVELOPE_CONSUMPTION

## Sealed
- RuntimeAshInferenceOutputTelemetry
- RuntimeAshInferenceOutputEnvelope
- RuntimeAshStreamingTelemetryHeader
- causal_lm envelope preflight
- causal_lm envelope execution wrapper
- infer_entry envelope execution wrapper
- output telemetry validation
- orchestrator direct inference bridge

## Runtime policy
- AdapterEnabled requires attached_lora_ids
- AdapterEnabled requires runtime_registry_ready
- AdapterEnabled requires attachment_load_success
- BaseOnlyExplicit allows empty attached_lora_ids
- Rejected attachment cannot start inference
- Silent fallback rejects inference
- Target auto-remap rejects inference

## Telemetry
- attached_lora_ids
- missing_lora_ids
- runtime_registry_ready
- base_only_explicit
- silent_fallback_detected
- target_auto_remap_detected
- inference_started
- inference_completed

## Boundary
runtime consumes the envelope and executes inference through wrapper callbacks.
orchestrator_local prepares the envelope and reports telemetry.
ash_core does not execute inference, load LoRA weights, read pointers, or call runtime.

## Python
No Python validator is allowed for ASH-14.
