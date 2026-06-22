# ASH G114 R2 B R1 TRAIN

Source: G114 R2 B TRAIN

Local bake fix card only.

## Scope

G114 Parent CLI Surface Rebind /
G113 Evidence Alias Acceptance Fix /
No Commit No Checkpoint Finalize

## Confirmed failure

```text
Error: missing required argument --g112-r2-b-g111-consumption
```

## Cause

The G114 runtime source still required legacy G112 parent argument names for the parent evidence block, while the intended G114 operator command supplies G113 parent argument names.

## Fix

Added G113 parent argument aliases while preserving legacy aliases:

- --g113-r2-b-g112-consumption or --g112-r2-b-g111-consumption
- --g113-r2-b-g76-consumption or --g113-r2-b-g75-consumption or --g112-r2-b-g74-consumption
- --g113-r2-b-continuity or --g112-r2-b-continuity
- --g113-r2-b-decision-lineage or --g112-r2-b-decision-lineage
- --g113-r2-b-review-bridge or --g113-r2-b-decision-bridge or --g112-r2-b-decision-bridge
- --g113-r2-b-manual-binding or --g112-r2-b-manual-binding
- --g113-r2-b-review-seal or --g113-r2-b-pending-decision or --g112-r2-b-pending-decision
- --g113-r2-b-review-seal or --g113-r2-b-decision-readiness or --g112-r2-b-decision-readiness
- --g113-r2-b-no-approval-execution or --g112-r2-b-no-approval-execution
- --g113-r2-b-no-commit or --g112-r2-b-no-commit
- --g113-r2-b-no-checkpoint-finalize or --g112-r2-b-no-checkpoint-finalize
- --g113-r2-b-no-route-mutation or --g112-r2-b-no-route-mutation
- --g113-r2-b-forbidden-claim or --g112-r2-b-forbidden-claim

## Boundaries remain closed

- No grant selection
- No reject selection
- No grant execution
- No reject execution
- No approval execution
- No commit
- No resident buffer mutation
- No checkpoint finalize
- No production or runtime route mutation
- No quality claim
