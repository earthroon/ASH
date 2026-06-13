# ASH-BASETRAIN-GPU-01 Bake Report

## 확정

This bake adds the tensor group manifest parser execution seal.

## Added/updated files

- `crates/base_train/src/ash_basetrain_gpu_01_tensor_group_manifest_parser_execution.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_01_tensor_group_manifest_parser_execution.rs`
- `crates/base_train/src/ash_basetrain_gpu_00_atlas_group_streaming_weight_train_runtime_audit.rs` compatibility re-export
- `crates/base_train/src/lib.rs` module exports
- `crates/base_train/Cargo.toml` bin target
- `ASH_BASETRAIN_GPU_01_*` receipts/contracts/static checks

## 닫힌 경로

- Tensor upload
- GPU buffer creation
- Forward/backward
- Optimizer step
- Delta apply
- Weight commit
- Safetensors mutation
- Checkpoint finalization
