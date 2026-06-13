# ASH-12 RuntimeLoraAttachment loader connect / current pointer attach execution

## Status
PASS_STATIC / PENDING_RUNTIME_COMPILE / PASS_RUNTIME_LORA_ATTACHMENT_LOADER_CONNECT

## Sealed
- RuntimeLoraAttachmentLoadPlan
- RuntimeLoraAttachExecutionReport
- current pointer attach request -> load plan
- RuntimeLoraAttachment sidecar generation
- RuntimeLoraAttachment loader connection
- explicit base-only execution
- no-silent-fallback validation

## Runtime policy
- Promoted current pointer -> AdapterEnabled -> RuntimeLoraAttachment sidecar load
- current=None + explicit base-only -> BaseOnlyExplicit, no load
- current=None without explicit base-only -> Rejected
- load failure -> Rejected, no base fallback
- missing manifest/model/target path -> Rejected

## Guards
- no attach success without attached_lora_ids
- no adapter-enabled success without load attempt
- no base-only implicit fallback
- no target auto-remap
- no Python validator

## Boundary
artifact_store persists pointer.
orchestrator_local reads pointer and writes sidecar.
runtime consumes sidecar/load plan and calls the existing RuntimeLoraAttachment loader.
ash_core does not participate in execution.
