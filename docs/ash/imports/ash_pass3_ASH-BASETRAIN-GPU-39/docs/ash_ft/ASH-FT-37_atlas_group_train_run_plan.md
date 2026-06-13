# ASH-FT-37
## Atlas Group Train Run Plan / Schedule To Trainable Scope Seal

## SSOT
ASH-FT-37 binds the deterministic atlas group schedule, trainable tensor registry, memory budget registry, sequence pack, and loss contract into a train run manifest. It opens exactly one selected atlas group as trainable, freezes all unselected groups, and forbids full model trainable fallback.

## Confirmed boundary
- Train run plan creation is allowed.
- Trainable scope finalization for the selected group is allowed.
- Frozen scope finalization for all unselected groups is allowed.
- Sequence pack and loss contract binding is allowed.
- Batch policy planning is allowed.

## Forbidden
- Model forward.
- Real loss computation.
- Backward.
- Optimizer state allocation.
- Training.
- Optimizer step.
- Weight update.
- Delta packet creation.
- Shadow route.
- Runtime default apply.
- Checkpoint alias rebind.
- Promotion.
- Full model trainable fallback.

## Expected verdict
`PASS_ASH_FT37_ATLAS_GROUP_TRAIN_RUN_PLAN_SCHEDULE_TO_TRAINABLE_SCOPE`

## Next
ASH-FT-38 — Optimizer State Staging / Group-Local State Allocation Plan Seal.
