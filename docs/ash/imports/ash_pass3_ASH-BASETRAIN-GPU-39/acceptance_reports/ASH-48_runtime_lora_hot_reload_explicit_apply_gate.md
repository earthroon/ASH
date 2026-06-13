# ASH-48 Runtime LoRA Hot Reload / Explicit Apply Gate

## Status
PASS_ASH_48_RUNTIME_LORA_APPLY_PLAN

## Sealed
- AshRuntimeLoraApplyMode
- AshRuntimeLoraApplyRequestKind
- AshRuntimeLoraExplicitApplyRequest
- AshRuntimeLoraApplyGateDecision
- AshRuntimeLoraApplyBlockerKind
- AshRuntimeLoraApplyBlocker
- AshRuntimeLoraHotReloadCandidate
- AshRuntimeLoraHotReloadPreflight
- AshRuntimeLoraHotReloadApplyPlan
- AshRuntimeLoraPreviousAttachmentSnapshot
- AshRuntimeLoraApplyReceipt
- AshRuntimeLoraExplicitApplyGateReport
- explicit apply request gate
- runtime hot reload candidate
- blocker-based preflight
- plan-only non-mutation boundary
- apply receipt and previous attachment snapshot contract

## Policy
- Explicit request is required for CommitExplicitApply.
- BuildApplyPlan does not mutate runtime current pointer.
- Missing manifest / weights blocks ReadyForExplicitApply.
- Determinism failure blocks apply.
- Snapshot inconsistency blocks apply.
- Manual review safety seal blocks apply.
- Rollback preflight blocker blocks apply.
- Perf guard rejection blocks apply.
- Previous attachment snapshot is required before commit receipt.
- applied=true requires receipt.
- No SFT/DPO training execution.
- No silent current pointer correction.
- No LoRA attach/detach side effect in ash_core/orchestrator audit.
- No Python validator.

## Boundary
ASH-48 defines the runtime LoRA explicit apply gate, hot reload apply plan, blocker preflight, previous attachment snapshot, and receipt structures. Runtime mutation remains gated and must not occur without explicit request and PASS preflight. ASH-49 handles emergency rollback / runtime safe mode.
