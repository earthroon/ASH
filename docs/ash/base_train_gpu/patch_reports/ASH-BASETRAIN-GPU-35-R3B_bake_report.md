# ASH-BASETRAIN-GPU-35-R3B Bake Report

## Added

```txt
crates/base_train/src/ash_basetrain_gpu_35_r3b_atlas_group_tensor_key_join_adapter.rs
crates/base_train/src/bin/ash_basetrain_gpu_35_r3b_atlas_group_tensor_key_join_adapter.rs
acceptance_reports/ASH-BASETRAIN-GPU-35-R3B.md
artifacts/ASH_BASETRAIN_GPU_35_R3B_ATLAS_GROUP_TENSOR_KEY_JOIN_ADAPTER.json
artifacts/ASH_BASETRAIN_GPU_35_R3B_STATIC_CHECKS.txt
artifacts/ASH_BASETRAIN_GPU_35_R3B_BAKE_MANIFEST.json
```

## Static verdict

```txt
BLOCKED_NO_ATLAS_GROUP_PLAN_SOURCE
```

The static verdict is a valid sealed result because R3B requires explicit local source paths.

## Runtime contract

The runner accepts:

```txt
--atlas-plan-receipt <path>
--tensor-metadata-source <path>
--selected-group-index <usize>
--selected-group-id <string optional>
```

It writes:

```txt
artifacts/ASH_BASETRAIN_GPU_35_R3B_ATLAS_GROUP_TENSOR_KEY_JOIN_ADAPTER.json
```

and prints the same receipt to stdout.

## No-load boundary

R3B reads only the explicit JSON sources. It does not open the safetensors source shard, read header bytes, load tensor bytes, allocate GPU buffers, run forward/backward, create optimizers, or mutate checkpoints.
