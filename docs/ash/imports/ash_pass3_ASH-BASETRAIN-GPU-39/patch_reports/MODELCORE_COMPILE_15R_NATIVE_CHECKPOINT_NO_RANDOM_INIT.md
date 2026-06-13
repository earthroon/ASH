# MODELCORE-COMPILE-15R — Native Checkpoint No-Random Init / Smoke Load Memory Seal

## Purpose

Prevent native full-checkpoint loading from allocating large random GPU tensors before checkpoint weights are applied.

## Changed Files

- crates/model_core/src/model_layers.rs
- crates/model_core/src/reference_checkpoint.rs
- crates/lora_train/src/bin/lora_train.rs

## Changes

- Added checkpoint tensor constructors for `AshLinear` and `AshRmsNorm`.
- Rebuilt `load_full_checkpoint_into_model` to construct `AshModel` directly from checkpoint tensors instead of calling `AshModel::new`.
- Avoided `Tensor::random` allocations on the full checkpoint load path.
- Filled the bin-side `FeatureShardMeta.runtime_signal_metadata_path` field with `None`.

## Non-Goals

- No random initialization behavior change for fresh model construction via `AshModel::new`.
- No checkpoint schema changes.
- No LoRA config changes.
- No smoke/full dump runtime success claim in this bake environment.

## Validation

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_15R_lora_train_check.log"
cargo run --manifest-path ".\crates\lora_train\Cargo.toml" --bin lora_train -- ".\configs\lora_v5_guarded_dump_smoke.json" 6 2>&1 | Tee-Object ".\target\LORA_DUMP_SMOKE_15R_no_random_init.log"
```

Expected cleared runtime pattern:

```text
AshModel::new -> Tensor::random -> can't allocate buffer of size: 465567744
```
