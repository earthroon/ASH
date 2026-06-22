# ASH G112 R2 B TRAIN

Source: G111 R2 B TRAIN
Bridge lineage: G74-R2

Local bake card only.

## Scope

Operator Approval Queue To Explicit Approval Decision Candidate /
Manual Approval Ledger To Pending Decision Seal /
No Commit No Checkpoint Finalize

## G74 actual receipt names

G74 existing source is `ash_basetrain_gpu_70k_g74_r2_weight_mutation_candidate.rs`. This G112-B route keeps the requested approval-decision-candidate semantics while binding to the actual G74 weight mutation candidate receipts.

- ASH_BASETRAIN_GPU_70K_G74_R2_APPROVED_APPLY_CANDIDATE_CONSUMPTION_RECEIPT.json
- ASH_BASETRAIN_GPU_70K_G74_R2_WEIGHT_MUTATION_CANDIDATE_RECEIPT.json
- ASH_BASETRAIN_GPU_70K_G74_R2_SELECTED_GROUP_MUTATION_CANDIDATE_SEAL.json
- ASH_BASETRAIN_GPU_70K_G74_R2_DELTA_APPLY_CANDIDATE_TO_MUTATION_LINEAGE_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G74_R2_NO_DELTA_APPLY_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G74_R2_NO_WEIGHT_MUTATION_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G74_R2_NO_WEIGHT_COMMIT_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G74_R2_NO_CHECKPOINT_MUTATION_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G74_R2_NO_DEFAULT_ROUTE_MUTATION_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G74_R2_FORBIDDEN_CLAIM_AUDIT.json

## Boundaries

Opened:
- G111 operator approval queue / manual ledger consumption
- G74 approval decision candidate via actual weight mutation candidate evidence consumption
- pending decision seal
- decision candidate readiness

Closed:
- No approval execution
- No approval grant/reject finalization
- No auto commit
- No resident buffer mutation
- No weight commit
- No checkpoint finalize
- No production or runtime route mutation
- No quality claim
