# MODELCORE-COMPILE-15V — Feature Store Staging Buffer Bulk Shard Writer Seal

## Purpose

Replace row-by-row feature-store hidden staging in bridge dump mode with pending-batch hidden generation and bulk flat-buffer shard staging.

## Changed Files

- crates/model_core/src/reference_checkpoint.rs
- crates/lora_train/src/feature_store.rs
- crates/lora_train/src/bin/lora_train.rs

## Changes

- Added `ReferenceModel::forward_hidden_id_batches`.
- Sealed `token_seed` overflow with wrapping multiplication.
- Added `FeatureShardBuffer::push_hidden_rows` and `push_batch_hidden_rows`.
- Added token-count flush guard through `FeatureShardBuffer::should_flush`.
- Replaced row-by-row `flat_hidden` temporary Vec construction in `bin/lora_train.rs`.
- Preserved the existing FeatureShardMeta and safetensors tensor schema.
- Added `[bridge-staging]` and `[bridge-shard]` diagnostics.

## Non-Goals

- No NativeWgpuModel eager-load restoration.
- No feature-store manifest schema change.
- No config schema redesign.
- No full dump execution.

## Validation

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_15V_lora_train_check.log"
cargo run --manifest-path ".\crates\lora_train\Cargo.toml" --bin lora_train -- ".\configs\lora_v5_guarded_dump_smoke.json" 6 2>&1 | Tee-Object ".\target\LORA_DUMP_SMOKE_15V_staging_writer.log"
```
