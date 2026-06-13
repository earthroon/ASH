# ASH-FT-25 Acceptance Report

## Patch
ASH-FT-25  
Group-Local Forward Backward Executor / Frozen Context Training Seal

## Expected result
PASS_ASH_FT25_GROUP_LOCAL_FORWARD_BACKWARD_EXECUTOR_FROZEN_CONTEXT_TRAINING

## Confirmed by receipt
- ASH-FT-24 schedule loaded
- selected schedule group resolved
- selected group exists in FT-23 budget registry
- exactly one active trainable group enabled
- all non-selected groups remain frozen
- full model trainable remains false
- group-local forward smoke executed
- group-local backward smoke executed
- gradient finite check passed
- optimizer step did not occur
- weight update did not occur
- delta packet was not created
- base checkpoint mutation did not occur
- runtime default apply did not occur
- checkpoint alias rebind did not occur
- promotion did not occur

## Blocked condition
If ASH-FT-24 has no executable schedule, ASH-FT-25 emits BLOCKED_ASH_FT25_NO_EXECUTABLE_SCHEDULE and does not run forward/backward.

## Next
ASH-FT-26 — Group-Local Gradient Validation / Optimizer Dry-run Boundary Seal
