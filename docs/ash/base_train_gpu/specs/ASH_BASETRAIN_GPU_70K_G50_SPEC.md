# ASH-BASETRAIN-GPU-70K-G50

## Patch

```text
ASH-BASETRAIN-GPU-70K-G50
Group Local Forward Logits Smoke /
Selected Group Resident Candidate To Group Local Logits Candidate Seal
No Decode No Sampling No Loss No Backward No Optimizer
```

## Commit

```text
commit: ASH-BASETRAIN-GPU-70K-G50
title: Group Local Forward Logits Smoke
message: base_train: add group local forward logits smoke candidate
```

## Purpose

G50 consumes the G49 selected atlas group resident candidate and creates a group-local forward logits candidate receipt. This patch opens only the forward/logits candidate surface. It does not decode, sample, generate text, compute loss, run backward, run optimizer, mutate weights, or write checkpoints.

## Required SSOT Inputs

```text
specs/ASH_BASETRAIN_GPU_70K_G49_SELECTED_ATLAS_GROUP_CHOICE_RECEIPT.json
specs/ASH_BASETRAIN_GPU_70K_G49_SELECTED_ATLAS_GROUP_RESIDENT_CANDIDATE_RECEIPT.json
artifacts/ash_ft/ash_ft00_full_coverage_manifest.json
artifacts/ash_ft/ash_ft00_atlas_group_plan.json
artifacts/ash_ft/ash_ft11_shadow_loader_plan.json
```

Runtime PASS additionally requires an explicit local forward fixture or input token window. G50 must not fabricate a fixture.

## State Ownership

G50 writes only JSON receipts under `specs/`. It does not mutate runtime default route state, checkpoint state, optimizer state, model weights, tokenizer state, or training state.

## New Source Files

```text
crates/base_train/src/ash_basetrain_gpu_70k_g50_group_local_forward_logits_smoke.rs
crates/base_train/src/bin/ash_basetrain_gpu_70k_g50_group_local_forward_logits_smoke.rs
```

## Cargo Bin

```toml
[[bin]]
name = "ash_basetrain_gpu_70k_g50_group_local_forward_logits_smoke"
path = "src/bin/ash_basetrain_gpu_70k_g50_group_local_forward_logits_smoke.rs"
```

## Receipts

```text
specs/ASH_BASETRAIN_GPU_70K_G50_GROUP_LOCAL_FORWARD_INPUT_PACKET.json
specs/ASH_BASETRAIN_GPU_70K_G50_SELECTED_GROUP_FORWARD_DISPATCH_CANDIDATE.json
specs/ASH_BASETRAIN_GPU_70K_G50_GROUP_LOCAL_LOGITS_CANDIDATE_RECEIPT.json
specs/ASH_BASETRAIN_GPU_70K_G50_SELECTED_GROUP_RESIDENT_LINEAGE_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G50_FORWARD_LOGITS_SHAPE_FINITE_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G50_NO_DECODE_SAMPLING_GENERATION_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G50_NO_LOSS_BACKWARD_OPTIMIZER_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G50_NO_CHECKPOINT_WEIGHT_MUTATION_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G50_FORBIDDEN_CLAIM_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G50_STATIC_CHECKS.json
specs/ASH_BASETRAIN_GPU_70K_G50_BAKE_MANIFEST.json
specs/ASH_BASETRAIN_GPU_70K_G50_LOCAL_BAKE_VALIDATION.json
```

## PASS Target

```text
PASS_ASH_BASETRAIN_GPU_70K_G50_GROUP_LOCAL_FORWARD_LOGITS_SMOKE
```

PASS requires G49 PASS lineage, explicit `selected_group_id=vocab_row_group__lm_head_weight`, `lm_head.weight` membership in the selected group, explicit fixture/input-window binding, logits candidate metadata generation, and `boundary_failures=0`.

## Forbidden Boundaries

```text
decode_executed=false
sampling_executed=false
generation_executed=false
text_output_created=false
loss_computed=false
backward_executed=false
optimizer_executed=false
checkpoint_mutated=false
weight_mutated=false
full_safetensors_payload_read=false
full_checkpoint_loaded=false
full_tensor_materialized=false
```

## Runtime CLI

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g50_group_local_forward_logits_smoke -- `
  --local-root . `
  --selected-group-id vocab_row_group__lm_head_weight `
  --forward-fixture .\artifacts\<local_forward_fixture>.json `
  --out-dir specs
```

Explicit binding form:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g50_group_local_forward_logits_smoke -- `
  --g49-selected-group-choice .\specs\ASH_BASETRAIN_GPU_70K_G49_SELECTED_ATLAS_GROUP_CHOICE_RECEIPT.json `
  --g49-resident-candidate .\specs\ASH_BASETRAIN_GPU_70K_G49_SELECTED_ATLAS_GROUP_RESIDENT_CANDIDATE_RECEIPT.json `
  --tensor-group-manifest .\artifacts\ash_ft\ash_ft00_full_coverage_manifest.json `
  --atlas-group-plan .\artifacts\ash_ft\ash_ft00_atlas_group_plan.json `
  --sequential-load-plan .\artifacts\ash_ft\ash_ft11_shadow_loader_plan.json `
  --selected-group-id vocab_row_group__lm_head_weight `
  --forward-fixture .\artifacts\<local_forward_fixture>.json `
  --out-dir specs
```

## Next Patch

```text
ASH-BASETRAIN-GPU-70K-G51
Group Local Finite Loss Candidate /
Forward Logits Candidate To Finite Loss Candidate Seal
No Backward No Optimizer No Weight Commit
```
