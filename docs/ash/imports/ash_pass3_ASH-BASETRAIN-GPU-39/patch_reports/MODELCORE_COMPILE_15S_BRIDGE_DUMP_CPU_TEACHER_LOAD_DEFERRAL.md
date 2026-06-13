# MODELCORE-COMPILE-15S — Bridge Dump CPU Teacher / Native GPU Load Deferral Seal

## Purpose

Prevent `bridge_dump_only` smoke runs from eagerly loading the full TinyLlama checkpoint into the native WGPU model before feature shard extraction.

The previous runtime panic happened after random initialization was removed: the next failure was a `Tensor::from_data` allocation while uploading full checkpoint tensors to GPU through `NativeWgpuModel::from_full_checkpoints`.

## Changed Files

- `crates/lora_train/src/bin/lora_train.rs`

## Changes

- Replaced the shared-hidden bridge dump teacher from `NativeWgpuModel::from_full_checkpoints(...)` to `model_core::ReferenceModel::new(...)` in the non-module-local `bridge_dump_only` path.
- Configured the compact reference teacher to emit the real manifest hidden size so existing feature shard shape contracts remain unchanged.
- Preserved `teacher_full_model_path` in the feature manifest as metadata only.
- Added an explicit runtime log line: `teacher_runtime=reference_compact_cpu native_gpu_load=deferred`.
- Did not change full training / non-bridge native GPU load paths.

## Non-Goals

- No model_core schema changes.
- No full checkpoint tensor upload changes.
- No smoke/full config path changes.
- No rows-per-shard or teacher batch size changes.
- No full dump execution claim.

## Validation

Run:

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_15S_lora_train_check.log"
```

Then smoke:

```powershell
cargo run --manifest-path ".\crates\lora_train\Cargo.toml" --bin lora_train -- ".\configs\lora_v5_guarded_dump_smoke.json" 6 2>&1 | Tee-Object ".\target\LORA_DUMP_SMOKE_15S_cpu_teacher.log"
```

Expected cleared patterns:

```text
NativeWgpuModel::from_full_checkpoints
checkpoint_tensor_2d
Tensor::from_data
can't allocate buffer
```

Expected new log:

```text
teacher_runtime=reference_compact_cpu native_gpu_load=deferred
```
