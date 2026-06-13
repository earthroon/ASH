# ASH-11 Runtime Current Pointer Consumption / Explicit Base-Only Gate

## Status
PASS_STATIC / PASS_RUNTIME_CURRENT_POINTER_EXPLICIT_BASE_ONLY_GATE

## Sealed
- current_adapter pointer consumption
- RuntimeAshCurrentAdapterPointer
- RuntimeAshPointerMode
- RuntimeExplicitBaseOnlyRequest
- RuntimeCurrentPointerHealthReport
- RuntimeCurrentPointerAttachRequest
- explicit base-only gate
- orchestrator_local current pointer reader bridge

## Pointer policy
- Promoted current pointer -> AdapterEnabled
- current=None + explicit base-only -> BaseOnlyExplicit
- current=None without explicit base-only -> Rejected
- Rejected/Pending/RollbackRequired current pointer -> Rejected
- missing manifest/model path -> Rejected

## Guards
- no silent base fallback
- no adapter_enabled without adapter_id
- no current attach unless status=Promoted
- no attach request from rejected health report
- Python validator forbidden

## Boundary
artifact_store persists pointers.
orchestrator_local reads pointers.
runtime consumes pointer DTO and validates attach readiness.
ash_core does not read pointer files.
