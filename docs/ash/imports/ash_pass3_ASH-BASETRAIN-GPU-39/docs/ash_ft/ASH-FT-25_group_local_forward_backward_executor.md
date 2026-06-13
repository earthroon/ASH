# ASH-FT-25
## Group-Local Forward Backward Executor / Frozen Context Training Seal

SSOT: ASH-FT-25 opens exactly one scheduled atlas group from ASH-FT-24 as the transient active trainable group, keeps all other groups frozen/read-only, and produces group-local forward/backward smoke plus gradient health receipts. It must not execute optimizer step, mutate weights, create delta packets, append delta stack, mutate base checkpoint, rebind runtime default, or promote a candidate.

## Required base
- ASH-FT-24 deterministic training schedule
- ASH-FT-23 group memory budget registry
- model manifest and safetensors manifest for identity validation

## Allowed
- Read FT-24 schedule
- Read FT-23 budget registry
- Resolve one scheduled group by order index
- Activate a transient single-group trainable scope
- Run bounded group-local forward/backward smoke
- Create gradient finite/norm receipt
- Write ASH-FT-25 receipts

## Forbidden
- Full model trainable
- More than one active trainable group
- Unrelated group gradient
- Full gradient allocation
- Full optimizer state allocation
- Optimizer step
- Weight update
- Delta packet creation
- Delta stack append
- Base checkpoint mutation
- Runtime default apply
- Checkpoint alias rebind
- Promotion
- Generation/sampling/token selection

## Expected pass
PASS_ASH_FT25_GROUP_LOCAL_FORWARD_BACKWARD_EXECUTOR_FROZEN_CONTEXT_TRAINING

## Blocked status
BLOCKED_ASH_FT25_NO_EXECUTABLE_SCHEDULE

## Next
ASH-FT-26 — Group-Local Gradient Validation / Optimizer Dry-run Boundary Seal
