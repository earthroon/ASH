# MODELCORE-COMPILE-15W — GPU Compact Teacher Kernel / CPU Hidden Loop Eviction Seal

## Purpose

Move compact teacher hidden generation for bridge dump mode behind an opt-in GPU compact dispatch path while keeping full native model loading deferred.

## Changed Files

- crates/burn_webgpu_backend/src/compact_teacher.rs
- crates/burn_webgpu_backend/src/lib.rs
- crates/model_core/src/native_wgpu.rs
- crates/lora_train/src/feature_store.rs
- crates/lora_train/src/bin/lora_train.rs

## Changes

- Added a WGSL compact teacher kernel that generates `[total_tokens, hidden_size]` pseudo hidden states from token/position/dim hash mixing.
- Added `NativeCompactTeacherRuntime` wrapper in model_core.
- Added `FeatureShardBuffer::push_flat_hidden_batch` for direct flat hidden staging.
- Added opt-in `ASH_LORA_COMPACT_GPU_TEACHER=1` bridge dump path.
- Preserved `native_gpu_load=deferred`; no `NativeWgpuModel::from_full_checkpoints` is used for bridge dump smoke.
- Added `[bridge-gpu-compact]` diagnostics and explicit fallback logging.

## Non-Goals

- No full checkpoint GPU loading.
- No feature store schema changes.
- No tokenizer/config path changes.
- No full dump execution.

## Validation

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_15W_lora_train_check.log"
$env:ASH_LORA_COMPACT_GPU_TEACHER="1"
cargo run --manifest-path ".\crates\lora_train\Cargo.toml" --bin lora_train -- ".\configs\lora_v5_guarded_dump_smoke.json" 6 2>&1 | Tee-Object ".\target\LORA_DUMP_SMOKE_15W_gpu_compact.log"
```
