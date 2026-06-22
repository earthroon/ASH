# ASH G114 R2 B TRAIN

Source: G113 R2 B TRAIN
Bridge lineage: G76-R2

Local bake card only.

## Scope

Grant-Reject Review Candidate To Explicit Operator Choice Candidate /
Decision Review Gate To Pending Choice Ledger Seal /
No Commit No Checkpoint Finalize

## G76 actual receipt names

G76 existing source is `ash_basetrain_gpu_70k_g76_r2_delta_apply_execution_candidate.rs`. This G114-B route keeps the requested operator-choice-candidate semantics while binding to the actual G76 delta apply execution candidate receipts.

- ASH_BASETRAIN_GPU_70K_G76_R2_MUTATION_PREFLIGHT_CONSUMPTION_RECEIPT.json
- ASH_BASETRAIN_GPU_70K_G76_R2_DELTA_APPLY_EXECUTION_CANDIDATE_RECEIPT.json
- ASH_BASETRAIN_GPU_70K_G76_R2_SELECTED_GROUP_APPLY_EXECUTION_CANDIDATE_SEAL.json
- ASH_BASETRAIN_GPU_70K_G76_R2_PREFLIGHT_TO_EXECUTION_CANDIDATE_LINEAGE_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G76_R2_EXECUTION_CANDIDATE_READINESS_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G76_R2_NO_DELTA_APPLY_EXECUTION_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G76_R2_NO_WEIGHT_MUTATION_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G76_R2_NO_WEIGHT_COMMIT_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G76_R2_NO_CHECKPOINT_MUTATION_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G76_R2_NO_DEFAULT_ROUTE_MUTATION_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G76_R2_FORBIDDEN_CLAIM_AUDIT.json

## Boundaries

Opened:
- G113 grant/reject review candidate consumption
- G76 explicit operator choice candidate via actual delta apply execution candidate evidence consumption
- pending choice ledger readiness
- operator choice candidate bridge

Closed:
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
