# ASH-13 Runtime current attachment into inference request / attached_lora telemetry seal

## Status
PASS_STATIC / PASS_RUNTIME_CURRENT_ATTACHMENT_INFERENCE_TELEMETRY

## Sealed
- RuntimeAshInferenceAttachmentMode
- RuntimeAshInferenceAttachmentMetadata
- RuntimeAshInferenceRequestEnvelope
- RuntimeAshInferenceAttachmentReport
- attach execution report -> inference metadata
- inference metadata validation
- attached_lora telemetry propagation
- base-only explicit inference gate
- orchestrator inference attachment report bridge

## Runtime policy
- AdapterEnabled requires attached_lora_ids
- AdapterEnabled requires runtime_registry_ready
- AdapterEnabled requires completed attachment load
- BaseOnlyExplicit allows empty attached_lora_ids
- BaseOnlyExplicit forbids attachment load attempt
- Rejected attachment cannot become inference request
- Silent fallback rejects inference request
- Target auto-remap rejects inference request

## Telemetry
- attached_lora_ids
- missing_lora_ids
- runtime_registry_ready
- base_only_explicit
- silent_fallback_detected
- target_auto_remap_detected
- attachment_load_attempted
- attachment_load_success

## Guards
- no inference envelope from rejected attachment
- no AdapterEnabled inference with empty attached_lora_ids
- no AdapterEnabled inference with runtime_registry_ready=false
- no BaseOnlyExplicit inference with load attempt
- no silent fallback pass
- no target auto-remap pass
- Python validator forbidden

## Boundary
artifact_store persists pointer.
orchestrator_local prepares inference attachment envelope/report.
runtime validates attachment telemetry.
ash_core does not execute inference.
