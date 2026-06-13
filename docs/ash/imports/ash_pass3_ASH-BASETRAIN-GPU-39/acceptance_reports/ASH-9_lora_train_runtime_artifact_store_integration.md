# ASH-9 lora_train/runtime/artifact_store integration

## Status
PASS_STATIC / PASS_ASH_EXECUTION_CRATE_INTEGRATION

## Sealed
- runtime ash attachment bridge
- lora_train curriculum bridge
- artifact_store promotion record bridge
- orchestrator_local ash API integration

## Runtime bridge
- consumes `AshRuntimeAttachmentPlanDto`
- preserves `forbid_silent_fallback`
- preserves `forbid_target_auto_remap`
- rejects adapter-enabled plans without adapter entries
- accepts explicit base-only plans without adapter entries

## lora_train bridge
- consumes `CurriculumRoute`
- maps `LmHead` to `lm_head`
- maps attention/ffn capability targets to module names
- refuses to silently remap `RuntimePolicy` / `RouterPolicy` to `lm_head`
- keeps unsupported targets explicit

## artifact_store bridge
- persists promotion decision metadata
- persists status patch metadata
- rejects promoted status without `Promote` decision
- rejects rollback-required records that remain promoted

## orchestrator_local bridge
- calls `ash_core` public API
- converts runtime route to execution-facing report
- converts curriculum route to training-facing report
- converts eval packet to promotion decision report

## Guards
- ash_core still has no runtime/lora_train/artifact_store dependency
- runtime preserves no-silent-fallback flags
- lora_train does not silently remap RuntimePolicy to lm_head
- artifact_store does not promote without decision
- orchestrator_local calls ash_core public API instead of internal modules
- Python validator forbidden

## Boundary
ash_core decides.
execution crates execute.
artifact_store persists.
orchestrator_local connects.
