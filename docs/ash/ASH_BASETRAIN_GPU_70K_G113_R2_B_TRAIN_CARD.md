# ASH G113 R2 B TRAIN

Source: G112 R2 B TRAIN
Bridge lineage: G75-R2

Local bake card only.

## Scope

Explicit Approval Decision Candidate To Operator Decision Review Gate /
Pending Decision Seal To Grant-Reject Review Candidate /
No Commit No Checkpoint Finalize

## G75 actual receipt names

G75 existing source is `ash_basetrain_gpu_70k_g75_r2_mutation_execution_preflight.rs`. This G113-B route keeps the requested operator-decision-review semantics while binding to the actual G75 mutation execution preflight receipts.

- ASH_BASETRAIN_GPU_70K_G75_R2_WEIGHT_MUTATION_CANDIDATE_CONSUMPTION_RECEIPT.json
- ASH_BASETRAIN_GPU_70K_G75_R2_MUTATION_EXECUTION_PREFLIGHT_RECEIPT.json
- ASH_BASETRAIN_GPU_70K_G75_R2_SELECTED_GROUP_MUTATION_SAFETY_GATE_RECEIPT.json
- ASH_BASETRAIN_GPU_70K_G75_R2_MUTATION_CANDIDATE_SAFETY_VERIFICATION_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G75_R2_MUTATION_CANDIDATE_TO_PREFLIGHT_LINEAGE_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G75_R2_NO_DELTA_APPLY_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G75_R2_NO_WEIGHT_MUTATION_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G75_R2_NO_WEIGHT_COMMIT_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G75_R2_NO_CHECKPOINT_MUTATION_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G75_R2_NO_DEFAULT_ROUTE_MUTATION_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G75_R2_FORBIDDEN_CLAIM_AUDIT.json

## Boundaries

Opened:
- G112 approval decision candidate / pending decision seal consumption
- G75 operator decision review gate via actual mutation execution preflight evidence consumption
- grant/reject review candidate readiness

Closed:
- No grant execution
- No reject execution
- No approval execution
- No approval decision finalization
- No commit
- No resident buffer mutation
- No checkpoint finalize
- No production or runtime route mutation
- No quality claim
