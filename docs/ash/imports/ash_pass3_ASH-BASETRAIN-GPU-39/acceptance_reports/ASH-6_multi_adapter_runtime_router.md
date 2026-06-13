# ASH-6 Multi-Adapter Runtime Router

## Status
PASS_STATIC / PASS_ASH_MULTI_ADAPTER_RUNTIME_ROUTER

## Sealed
- RuntimeRouteIntent
- RuntimeRouterInput
- RuntimeAdapterRoute
- AdapterConflictPolicy
- RuntimeRouterPolicy
- RuntimeRouterOutput
- RuntimeRouterStatus
- route_runtime_adapters(...)
- runtime_routes_to_attachment_plan(...)

## Routing
- KoreanDialogue -> korean_response_stability -> ash_lm_head_lora_promoted
- RuntimeAttachCheck -> runtime_attach_integrity -> ash_lm_head_lora_promoted
- BaseOnlyExplicit -> no adapters
- TechnicalDebugging without logic adapter -> rejected or manual review, no silent style fallback

## Guards
- only promoted adapters enabled by default
- candidate adapters blocked unless explicitly allowed
- same target conflict guarded
- no silent fallback
- no target auto-remap
- no missing adapter pass
- Python validator forbidden

## Boundary
ash_core emits runtime route and attachment plan only.
ash_core does not load adapter weights.
ash_core does not run runtime forward.
ash_core does not import runtime/model_core/lora_train/artifact_store.
