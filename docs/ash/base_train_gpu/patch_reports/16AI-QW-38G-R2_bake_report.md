# 16AI-QW-38G-R2 Bake Report

Patch: `16AI-QW-38G-R2 — Live Heartbeat & Hook Reachability / Fail-Closed Receipt Seal`

## Base
`ash_pass3_16AI-QW-38G-R1_rust_native_trace_baked.zip`

## Files changed
- `crates/runtime/src/infer.rs`
  - Added runtime entry heartbeat helpers.
  - Added fail-closed receipt writer.
  - Added start/env/model/tokenizer/prompt/generation/backend/done heartbeat stages.
  - Final receipt classifies missing layerwise trace as `FAIL_LAYERWISE_HOOK_NOT_REACHED` instead of silent failure.
- `crates/model_core/src/native_wgpu.rs`
  - Added R2 `native_forward_enter` and `hook_attempt` logs.
  - Updated layerwise runtime receipt patch id to R2.
- `scripts/run_16AI_QW_38G_layerwise_reserved_direction.ps1`
  - Uses release build once.
  - Runs `infer_only.exe` live with `Tee-Object` by default.
  - Keeps `-Quiet` option for file-only mode.
  - Prints receipt and warns if trace/summary are missing.

## Validation
- Static string validation: PASS
- Cargo check: NOT_RUN_CONTAINER_CARGO_UNAVAILABLE

## Expected runtime outputs
- `workspace/infer_qw38g_live_console.log`
- `workspace/qw38g_runtime_receipt.json`
- Optional if hook reaches layerwise path:
  - `workspace/qw38g_layerwise_reserved_direction_trace.jsonl`
  - `workspace/qw38g_layerwise_reserved_direction_summary.json`

## Notes
R2 is not a deeper analysis patch. It is a reachability and fail-closed visibility patch. It prevents silent failures by writing a receipt even when the layerwise hook is not reached.
