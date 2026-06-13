# ASH-21 Composite Adapter Promotion / Rollback Gate

## Status
PASS_COMPOSITE_ADAPTER_PROMOTION_ROLLBACK_GATE

## Sealed
- AshCompositePromotionMode
- AshCompositeAdapterProfileStatus
- AshCompositeAdapterWeight
- AshCompositeAdapterProfile
- AshCompositePromotionGateConfig
- AshCompositePromotionReport
- AshCompositePointerState
- AshCompositeRollbackMode
- AshCompositeRollbackReason
- AshCompositeRollbackReport
- promotion candidate validation
- promote-to-current pointer gate
- rollback-to-previous-stable gate
- orchestrator CLI-safe promotion/rollback report

## Policy
- ASH-21 does not merge LoRA tensors.
- ASH-21 does not train LoRA.
- SoftEnsemble route becomes composite profile evidence.
- Phase route becomes promotion safety evidence.
- Base-only route cannot be promoted.
- Current pointer changes only through explicit PromoteToCurrent.
- PromoteToCurrent requires a previous stable pointer snapshot.
- Rollback only targets previous stable pointer.
- No fallback pointer is invented.
- No Python validator is added.

## Boundary
ash_core computes promotion and rollback reports.
runtime executes promoted profile attachments later.
orchestrator_local reports audit evidence.
artifact_store preserves pointer snapshots and reports later.
