# ASH-BASETRAIN-GPU-36 Bake Report

## Result

Baked as a read-only preflight patch on top of `ASH-BASETRAIN-GPU-35-R3B`, with Rust control-flow rebased to lookup-table/combinator style and no `if` / `match` keyword usage in the ASH-BASETRAIN-GPU-36 Rust runner/module.

## Added code

- `crates/base_train/src/ash_basetrain_gpu_36_selected_group_weight_slice_load_preflight.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_36_selected_group_weight_slice_load_preflight.rs`

## Static receipt

- `artifacts/ASH_BASETRAIN_GPU_36_SELECTED_GROUP_WEIGHT_SLICE_LOAD_PREFLIGHT.json`
- static status: `BLOCKED_R3B_RECEIPT_NOT_FOUND`

## Why static BLOCKED is expected

The bake container does not provide a local explicit R3B PASS receipt path. The runner is intentionally source-explicit and does not guess a receipt path.

## Local validation command

```powershell
cargo build -p base_train --bin ash_basetrain_gpu_36_selected_group_weight_slice_load_preflight
cargo run -p base_train --bin ash_basetrain_gpu_36_selected_group_weight_slice_load_preflight -- --r3b-receipt .rtifacts\ASH_BASETRAIN_GPU_35_R3B_ATLAS_GROUP_TENSOR_KEY_JOIN_ADAPTER.json
```

## Guard status

No tensor bytes are read. No file is opened. No GPU is requested. No optimizer/backward/mutation path is touched. The 36 Rust files were statically grepped for standalone `if` / `match` keywords and returned no hits.
