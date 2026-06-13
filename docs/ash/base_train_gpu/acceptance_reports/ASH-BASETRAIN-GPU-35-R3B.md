# ASH-BASETRAIN-GPU-35-R3B Acceptance Report

## Patch

**ASH-BASETRAIN-GPU-35-R3B**  
Atlas Group Tensor Key Join Adapter / Group Plan Entry To Tensor Metadata Source Join No Weight Load Seal

## Purpose

R3B joins an explicit atlas group plan entry with an explicit tensor metadata source. It derives a selected group manifest candidate from:

- `groups[].tensor_keys[]` in the atlas group plan
- `tensors[].tensor_key` in the full coverage manifest
- `source_candidate` in the metadata source

No value is invented. Estimated memory budget fields are never promoted to byte ranges.

## Static baked result

The static baked receipt is intentionally sealed as:

```txt
BLOCKED_NO_ATLAS_GROUP_PLAN_SOURCE
```

This is valid for the bake container because the canonical local files are not bundled in this ZIP and must be supplied by explicit CLI arguments on the operator machine.

## Expected local PASS command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_35_r3b_atlas_group_tensor_key_join_adapter -- --atlas-plan-receipt .\artifacts\ash_ft\ash_ft00_atlas_group_plan.json --tensor-metadata-source .\artifacts\ash_ft\ash_ft00_full_coverage_manifest.json --selected-group-index 0
```

Expected PASS status when local sources match the observed SSOT:

```txt
PASS_ASH_BASETRAIN_GPU_35_R3B_ATLAS_GROUP_TENSOR_KEY_JOIN_ADAPTER_GROUP_PLAN_ENTRY_TO_TENSOR_METADATA_SOURCE_JOIN_NO_WEIGHT_LOAD
```

## Required observed SSOT for selected group index 0

```txt
group_id = vocab_row_group__model_embed_tokens_weight
tensor_key = model.embed_tokens.weight
dtype = F32
shape = [48259, 2048]
element_count = 98834432
expected_byte_size = 395337728
byte_offsets.file_start = 395361664
byte_offsets.file_end = 790699392
source_candidate.sha256_matches = true
runtime_default_apply_allowed = false
```

## Guards

```txt
invented_shape=false
invented_dtype=false
invented_byte_range=false
invented_tensor_name=false
invented_source_shard_path=false
estimated_budget_used_as_byte_range=false
selected_group_weights_loaded=false
safetensors_header_read_executed=false
runtime_gpu_buffer_created=false
wgpu_device_requested=false
forward_executed=false
selected_group_backward_executed=false
optimizer_created=false
optimizer_step_executed=false
delta_candidate_materialized=false
checkpoint_write_executed=false
safetensors_mutation_present=false
runtime_1p1b_training_claimed=false
```

## Next

- PASS -> `ASH-BASETRAIN-GPU-36`
- multi tensor group block -> `ASH-BASETRAIN-GPU-35-R3B-R1`
- metadata schema block -> `ASH-BASETRAIN-GPU-35-R3B-R2`
- source candidate block -> `ASH-BASETRAIN-GPU-35-R3B-R3`
