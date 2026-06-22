# ASH G109 R2 B TRAIN

Source: G108 R2 B TRAIN
Bridge lineage: G71-R2

Local bake card only.

## Scope

Weight Delta Candidate To Isolated Delta Apply Candidate /
Selected Group Delta Candidate To Non-Commit Apply Readiness Seal /
No Weight Commit No Checkpoint Finalize

## G71 actual receipt names

- ASH_BASETRAIN_GPU_70K_G71_R2_DELTA_CANDIDATE_INTEGRITY_REVIEW_RECEIPT.json
- ASH_BASETRAIN_GPU_70K_G71_R2_DELTA_APPLY_REVIEW_GATE_RECEIPT.json
- ASH_BASETRAIN_GPU_70K_G71_R2_DELTA_APPLY_CANDIDATE_ALLOWED_RECEIPT.json
- ASH_BASETRAIN_GPU_70K_G71_R2_OPERATOR_APPROVAL_REQUIRED_RECEIPT.json
- ASH_BASETRAIN_GPU_70K_G71_R2_DELTA_REVIEW_LINEAGE_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G71_R2_NO_DELTA_APPLY_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G71_R2_NO_WEIGHT_MUTATION_AUDIT.json
- ASH_BASETRAIN_GPU_70K_G71_R2_NO_DEFAULT_ROUTE_MUTATION_AUDIT.json

## Boundaries

Opened:
- G108 selected group delta candidate consumption
- G71 delta apply review gate and candidate allowed evidence consumption
- isolated apply non-commit readiness

Closed:
- No resident buffer mutation
- No weight commit
- No checkpoint finalize
- No production or runtime route mutation
- No quality claim
