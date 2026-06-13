# MODELCORE-COMPILE-13T-F — ReferenceModel Bridge API / FeatureShardMeta Seal

## Purpose

Restore the narrow ReferenceModel APIs required by `lora_train` feature capture and baseline weight lookup, and seal `FeatureShardMeta` initializer drift.

## Changed Files

- crates/model_core/src/reference_checkpoint.rs
- crates/lora_train/src/bridge.rs
- crates/lora_train/src/training.rs

## Changes

- Added `ReferenceModel::capture_module_io_padded_batch`.
- Added `ReferenceModel::capture_module_io_ids_batch`.
- Added `ReferenceModel::module_linear_weight`.
- Added an internal full-checkpoint accessor for ReferenceModel capture/weight paths.
- Added an internal padded-batch capture helper using the existing reference math helpers.
- Added `runtime_signal_metadata_path: None` to `FeatureShardMeta` initializers.
- Reapplied the prior training-scope seal where the physical 13T-E artifact was unavailable in the bake workspace.

## Non-Goals

- No orchestration runtime float inference fix.
- No `String.to_path_buf` fix.
- No Half/Cpu batch mismatch repair.
- No cli_vendor187 unsafe env repair.
- No module_local_batching ownership repair.
- No warning hygiene sweep.

## Validation

Run:

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_13T_F_lora_train_check.log"
```

Expected cleared patterns:

```text
capture_module_io_padded_batch
module_linear_weight
runtime_signal_metadata_path
```
