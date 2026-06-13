# ASH-43 Event Tag Runtime Router Integration

## Status
PASS_EVENT_TAG_RUNTIME_ROUTER_INTEGRATION

## Sealed
- AshEventTagRuntimeRouterMode
- AshRuntimeAdapterActivationAction
- AshRuntimeEventTagSignalSource
- AshRuntimeApplyReadiness
- AshRuntimeEventTagSignal
- AshRuntimeAdapterActivationScore
- AshRuntimeAdapterActivationDecision
- AshRuntimeAdapterActivationPlan
- AshRuntimeEventTagRouteAdjustmentCandidate
- AshRuntimeEventTagSoftEnsembleCandidate
- AshEventTagRuntimeRouterIntegrationReport
- runtime event to event tag signal mapping
- affinity / avoidance / temporal penalty scoring
- adapter activation decision
- route adjustment candidate
- soft ensemble candidate
- runtime activation view

## Policy
- ASH-43 does not run SFT
- ASH-43 does not export JSONL
- ASH-43 does not mutate adapter registry
- ASH-43 does not change current pointer
- ASH-43 does not hot reload runtime
- ASH-43 does not attach LoRA directly
- Runtime apply requires explicit apply
- runtime_apply_started must remain false
- Missing re-entry candidate blocks activation by default
- Temporal overlay is short-term; routing policy is long-term
- No Python validator

## Boundary
ash_core computes runtime activation decisions.
runtime exposes activation plan view only.
orchestrator_local reports integration evidence.
ASH-44 handles rollback lineage.
