# STAGE3 A/B PATCH REPORT

## Scope
- Stage3-A: add a native module-local trace seam for prepadded batches.
- Stage3-B: move bridge orchestration to a native-first runtime with reference fallback.

## Applied changes

### `crates/model_core/src/lib.rs`
- Added `ModuleTraceTapRequest` and `ModuleTraceTapResult` structs as stage3 trace seam types.
- Added `capture_module_from_native_hidden(...)` helper to materialize `[B, T, H]` tensors into `CapturedModuleIo` rows using `seq_lens`.
- Added `NativeWgpuModel::capture_module_io_native_padded_batch(...)`.
  - Supports `attn.q_proj`, `attn.o_proj`, and `ffn.up_proj`.
  - Uses `AshModel` native path directly (`embed -> input_norm/q_proj/...`) and captures tensors before/after the requested module.
  - Keeps padded batch ownership in the native path and avoids rebuilding `Vec<Vec<u32>>` at capture time.

### `crates/lora_train/src/bridge.rs`
- Added `ModuleLocalCaptureRuntime` enum.
  - `NativeFirst { native, fallback }`
  - `Reference(...)`
- Added `capture_padded_batch(...)` runtime dispatch.
  - Tries native capture first.
  - Falls back to reference capture if native trace fails.
- Updated module-local extraction to construct a native-first runtime when `model_kind = ash_native`.
- Updated capture loop to use runtime orchestration instead of calling the reference teacher directly.
- Added runtime selection / fallback logs:
  - `[bridge][module_local][runtime] selected mode=...`
  - `[bridge][module_local][runtime] native capture ok ...`
  - `[bridge][module_local][runtime] native capture fallback ...`

## Intended effect
- Stage1: prep/write overlap
- Stage2: prepadded batch handoff
- Stage3-A/B: native-first capture seam + bridge orchestration lowering

This should reduce the amount of CPU-side capture ownership and make the bridge behave more like an orchestrator than a compute owner.

## Limits
- Not compile-verified in this container because `cargo` / `rustc` are unavailable.
- Native capture seam currently targets the q/o/up subset only.
- Fallback path still loads and keeps a reference teacher for safety.
