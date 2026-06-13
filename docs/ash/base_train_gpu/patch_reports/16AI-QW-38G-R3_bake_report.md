# 16AI-QW-38G-R3 Bake Report

## Patch
`16AI-QW-38G-R3 — Native Forward Stage Map / Executed Path Discovery Seal`

## Base
`ash_pass3_16AI-QW-38G-R2_live_heartbeat_baked.zip`

## Files Changed
- `crates/model_core/src/native_wgpu.rs`
- `crates/runtime/src/infer.rs`
- `scripts/run_16AI_QW_38G_layerwise_reserved_direction.ps1`

## Files Added
- `acceptance_reports/16AI-QW-38G-R3_native_forward_stage_map.md`
- `patch_reports/16AI-QW-38G-R3_bake_report.md`
- `patch_reports/16AI-QW-38G-R3_native_wgpu.diff`
- `patch_reports/16AI-QW-38G-R3_infer.diff`
- `patch_reports/16AI-QW-38G-R3_runner.diff`
- `target/16AI-QW-38G-R3_static_validation.json`

## Implementation Summary
- Added Rust-native stage map registry in `native_wgpu.rs`.
- Added stage counters for generation/projection candidates:
  - `NativeWgpuModel::forward_logits_for_generation`
  - `NativeWgpuModel::forward_hidden_for_generation_input`
  - `NativeWgpuModel::project_last_hidden_to_logits_vocab_atlas`
  - `vocab_atlas_projection`
  - `raw_topk_trace_hook`
  - `hidden_projection_trace_hook`
  - `layerwise_reserved_trace_hook`
  - layer/attention/MLP/final norm candidates when reached.
- Added R3 runtime receipt writer in `infer.rs`.
- Updated runner to set `ASH_FORWARD_STAGE_MAP=1`, write R3 stage map and receipt, and stop relying on Python postprocess.

## Runtime Artifacts
Expected local outputs:
- `workspace/qw38g_r3_forward_stage_map.json`
- `workspace/qw38g_r3_runtime_receipt.json`
- `workspace/infer_qw38g_r3_stage_map_live.log`

## Validation
- Static validation: `PASS_STATIC`
- Cargo check: `NOT_RUN_CONTAINER_CARGO_UNAVAILABLE`

## Mutation Policy
- no weight mutation
- no tokenizer mutation
- no safetensors mutation
- no banlist mutation
