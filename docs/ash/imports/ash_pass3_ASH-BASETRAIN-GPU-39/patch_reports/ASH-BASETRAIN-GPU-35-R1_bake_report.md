# ASH-BASETRAIN-GPU-35-R1 Bake Report

- Added Rust source: `crates/base_train/src/ash_basetrain_gpu_35_r1_selected_group_manifest_binding.rs`
- Added bin: `crates/base_train/src/bin/ash_basetrain_gpu_35_r1_selected_group_manifest_binding.rs`
- Added manifest / shape / dtype / byte-range receipts.
- Default baked receipt is blocked safe no-manifest route.
- No runtime GPU allocation, selected group weight load, backward, optimizer, delta, checkpoint mutation.

Manifest binding chain digest default:

```txt
8f6dcaf534ce2bdec12670d3b4960bbf5e86bcaa3f315e73a0276d800bdd2b97
```
