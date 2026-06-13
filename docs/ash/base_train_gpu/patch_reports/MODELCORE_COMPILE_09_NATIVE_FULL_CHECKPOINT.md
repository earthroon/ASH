# MODELCORE-COMPILE-09 — Native Full Checkpoint Execution Path Contract

## Purpose

Define the full checkpoint execution contract without moving `ReferenceExecutionPath` ownership into `NativeWgpuModel`.

`ReferenceModel` owns reference execution orchestration. `NativeWgpuModel` may hold an explicit read-only `FullCheckpointWeights` attachment for native capture/dump paths.

## Changed Files

- `crates/model_core/src/reference_checkpoint.rs`
- `crates/model_core/src/native_wgpu.rs`

## Changes

- Added `ReferenceModel::forward_hidden_ids_full`.
- Added `ReferenceModel::forward_logits_ids_full`.
- Added `full_checkpoint_execution: Option<Arc<FullCheckpointWeights>>` to `NativeWgpuModel`.
- Added `attach_full_checkpoint_execution`.
- Added `full_checkpoint_execution_weights`.
- Replaced stale `self.execution_path` reads in native full-checkpoint capture/weight paths.
- Initialized native full checkpoint attachment from the loaded checkpoint without a large silent clone.
- Removed stale native-owned full-checkpoint forward helpers that belonged to the reference path contract.

## Non-Goals

- No runtime_lora schema repair.
- No generation_telemetry Result alias repair.
- No traces/severity ownership repair.
- No config changes.
- No silent fallback/no-op full checkpoint execution.

## Prohibited Shortcuts Avoided

- Did not re-add `execution_path` to `NativeWgpuModel`.
- Did not clone large full checkpoint weights silently.
- Did not return empty/default dump data when full checkpoint is unavailable.
- Did not move `ReferenceExecutionPath` ownership into native_wgpu.

## Validation

Run:

```powershell
cargo check -p model_core 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_09_check.log"
```

Expected cleared patterns:

```text
forward_hidden_ids_full
forward_logits_ids_full
no field `execution_path`
```

Allowed remaining patterns:

```text
generation_telemetry Result<T> E0107
generation_telemetry HashMap E0282
traces borrow E0505
severity moved E0382
```
