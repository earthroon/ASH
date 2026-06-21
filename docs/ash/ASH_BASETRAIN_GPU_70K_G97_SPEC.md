# ASH-BASETRAIN-GPU-70K-G97

## Runtime Candidate Route Attach Plan / Adopted Candidate State To Non-Default Runtime Route Candidate Seal

Seal: **No Weight Commit / No Checkpoint Mutation**

## Patch Identity

```text
PatchId: ASH-BASETRAIN-GPU-70K-G97
SourcePatchId: ASH-BASETRAIN-GPU-70K-G96
PreviousPassTarget: PASS_ASH_BASETRAIN_GPU_70K_G96_GUARDED_DELTA_PACKET_ADOPTION_EXECUTION
RuntimePassTarget: PASS_ASH_BASETRAIN_GPU_70K_G97_RUNTIME_CANDIDATE_ROUTE_ATTACH
NextPatch: ASH-BASETRAIN-GPU-70K-G98
```

G97 attaches the G96 adopted candidate state to a non-default runtime candidate route. This patch intentionally opens `runtime_candidate_route_attached == true` and `runtime_route_mutated == true`, while keeping `runtime_default_route_mutated == false`. It does not mutate default/production route, weights, weight commits, checkpoints, or optimizer state.

## SSOT Boundary

Input SSOT:

```text
ASH_BASETRAIN_GPU_70K_G96_GUARDED_DELTA_PACKET_ADOPTION_EXECUTION_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G96_ADOPTED_CANDIDATE_STATE.json
ASH_BASETRAIN_GPU_70K_G96_ADOPTION_ROLLBACK_ANCHOR.json
```

Output SSOT:

```text
ASH_BASETRAIN_GPU_70K_G97_RUNTIME_CANDIDATE_ROUTE_ATTACH_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G97_RUNTIME_CANDIDATE_ROUTE_STATE.json
ASH_BASETRAIN_GPU_70K_G97_RUNTIME_CANDIDATE_ROUTE_REGISTRY_PATCH.json
ASH_BASETRAIN_GPU_70K_G97_RUNTIME_CANDIDATE_ROUTE_ROLLBACK_ANCHOR.json
ASH_BASETRAIN_GPU_70K_G97_ROUTE_ATTACH_SCHEMA_AUDIT.json
ASH_BASETRAIN_GPU_70K_G97_ROUTE_ATTACH_LINEAGE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G97_ROUTE_ATTACH_BOUNDARY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G97_NO_DEFAULT_ROUTE_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G97_NO_WEIGHT_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G97_NO_WEIGHT_COMMIT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G97_NO_CHECKPOINT_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G97_FORBIDDEN_CLAIM_AUDIT.json
```

## Allowed True Flags

```text
actual_delta_packet_adopted == true
runtime_candidate_route_attached == true
runtime_route_mutated == true
```

## Still Forbidden

```text
runtime_default_route_mutated == false
runtime_adapter_route_mutated == false
production_route_mutated == false
default_inference_pointer_mutated == false
actual_weight_mutated == false
actual_weight_committed == false
actual_checkpoint_mutated == false
ledger_mutated_by_g97 == false
```

## Implementation Files

```text
crates/base_train/src/ash_basetrain_gpu_70k_g97_runtime_candidate_route_attach.rs
crates/base_train/src/bin/ash_basetrain_gpu_70k_g97_runtime_candidate_route_attach.rs
```

## CLI Contract

Required:

```text
--g96-adoption-execution-receipt <path>
--g96-adopted-candidate-state <path>
--g96-adoption-rollback-anchor <path>
--selected-group-id <string>
--runtime-candidate-route-id <string>
--out-dir <path>
```

Default policy:

```text
attach_non_default_runtime_candidate_route_only_no_default_route_no_weight_no_checkpoint
```

Default route id:

```text
runtime_candidate_route__vocab_row_group__lm_head_weight__g97
```

## Validation Gates

G97 verifies:

```text
G96 receipt PASS
G96 adopted candidate state digest stable and matching receipt
G96 adoption rollback anchor digest stable and matching receipt
actual_delta_packet_adopted == true
selected_group_id == vocab_row_group__lm_head_weight
runtime candidate route id is not default/production/current
route_attach_policy == attach_non_default_runtime_candidate_route_only_no_default_route_no_weight_no_checkpoint
```

## PASS Target

```text
PASS_ASH_BASETRAIN_GPU_70K_G97_RUNTIME_CANDIDATE_ROUTE_ATTACH
```

## Recommended Cargo Run

```powershell
$g96r = ".\artifacts\ASH_BASETRAIN_GPU_70K_G96_GUARDED_DELTA_PACKET_ADOPTION_EXECUTION_RECEIPT.json"
$state = ".\artifacts\ASH_BASETRAIN_GPU_70K_G96_ADOPTED_CANDIDATE_STATE.json"
$anchor = ".\artifacts\ASH_BASETRAIN_GPU_70K_G96_ADOPTION_ROLLBACK_ANCHOR.json"

cargo run -p base_train --bin ash_basetrain_gpu_70k_g97_runtime_candidate_route_attach -- `
  --g96-adoption-execution-receipt $g96r `
  --g96-adopted-candidate-state $state `
  --g96-adoption-rollback-anchor $anchor `
  --selected-group-id vocab_row_group__lm_head_weight `
  --runtime-candidate-route-id runtime_candidate_route__vocab_row_group__lm_head_weight__g97 `
  --out-dir .\artifacts
```

## Next Patch

```text
ASH-BASETRAIN-GPU-70K-G98
Runtime Candidate Route Shadow Evaluation /
Non-Default Candidate Route To Shadow Inference Probe Seal
No Default Route Mutation No Weight Commit No Checkpoint Mutation
```
