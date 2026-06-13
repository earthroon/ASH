# ASH-BASETRAIN-GPU-35-R3 Acceptance

## Patch

Selected Group Manifest From Atlas Plan Receipt / Derived Manifest Candidate No Invent No Weight Load Seal

## Confirmed

- R3 source module added: `crates/base_train/src/ash_basetrain_gpu_35_r3_selected_group_manifest_from_atlas_plan_receipt.rs`
- R3 binary wrapper added: `crates/base_train/src/bin/ash_basetrain_gpu_35_r3_selected_group_manifest_from_atlas_plan_receipt.rs`
- Existing receipt search roots are read-only.
- Selected group manifest candidate is derived only from parseable existing atlas/group/plan/receipt artifacts.
- Shape, dtype, byte range, tensor name, and source shard path are not invented.
- Weight load, GPU buffer creation, backward, optimizer, delta materialization, checkpoint write, and safetensors mutation remain closed.

## Baked static result in this ZIP

```txt
BLOCKED_NO_SELECTED_GROUP_ENTRY_FOUND
```

Reason: parseable atlas/group/plan candidate artifacts exist, including prior templates/skeletons, but this ZIP does not contain a complete selected group entry with direct `shape`, `dtype`, `byte range`, `tensor_name`, and `source_shard_path` metadata from an atlas group plan receipt.

## Guard receipt

```txt
invented_shape=false
invented_dtype=false
invented_byte_range=false
selected_group_weights_loaded=false
runtime_gpu_buffer_created=false
selected_group_gradient_buffer_allocated=false
selected_group_backward_executed=false
optimizer_step_executed=false
safetensors_mutation_present=false
runtime_1p1b_training_claimed=false
```

## Runtime/build note

- `cargo` and `rustc` are unavailable in this container, so local compile/run was not executed here.
- Static bake receipts were generated and included.

## Next route

- If a complete atlas group plan receipt is supplied: `ASH-BASETRAIN-GPU-36`
- If receipt path binding is still missing: `ASH-BASETRAIN-GPU-35-R3A`
