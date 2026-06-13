# 16AI-QW-38G-R6A Bake Report

## Patch
`16AI-QW-38G-R6A — Shader Dispatch Hook Exposure / Debug Buffer Binding Surface Seal`

## Base
`ash_pass3_16AI-QW-38G-R6_shader_debug_buffer_baked.zip`

## Changed Files
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38G_R6A_debug_binding.ps1`
- `acceptance_reports/16AI-QW-38G-R6A_shader_dispatch_hook_exposure.md`
- `patch_reports/16AI-QW-38G-R6A_bake_report.md`
- `patch_reports/16AI-QW-38G-R6A_native_wgpu.diff`
- `patch_reports/16AI-QW-38G-R6A_runner.ps1.snapshot`
- `target/16AI-QW-38G-R6A_static_validation.json`

## Implementation
R6A adds a Rust-native dry-run binding surface discovery path:

- `ASH_SHADER_DEBUG_BINDING=1`
- `ASH_SHADER_DEBUG_BINDING_DRY_RUN=1`
- `ASH_SHADER_DEBUG_BINDING_GROUP=auto`
- `ASH_SHADER_DEBUG_BINDING_SLOT=auto`
- `ASH_SHADER_DEBUG_BINDING_MAP=workspace/qw38g_r6a_debug_binding_map.json`
- `ASH_SHADER_DEBUG_BINDING_RECEIPT=workspace/qw38g_r6a_debug_binding_receipt.json`

The implementation does **not** perform shader writes. It records candidate availability and writes map/receipt. In the current hot path, direct bind group layout surface is expected to remain unavailable unless a later pipeline-layout registry exposes it.

## Safety
- No weight mutation
- No tokenizer mutation
- No safetensors mutation
- No banlist mutation
- No full activation readback
- Dry-run only by default

## Local Build Status
`cargo_check = NOT_RUN_CONTAINER_CARGO_UNAVAILABLE`

Static validation was performed by source inspection.
