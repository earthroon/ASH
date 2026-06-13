# 16AI-QW-38G-R6 Bake Report

## Patch
16AI-QW-38G-R6 — Shader Debug Buffer Design / Explicit Intermediate Export Candidate Seal

## Base
ash_pass3_16AI-QW-38G-R4_gpu_debug_tap_baked.zip

## Files Changed
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38G_R6_shader_debug_buffer.ps1`
- `acceptance_reports/16AI-QW-38G-R6_shader_debug_buffer_design.md`
- `patch_reports/16AI-QW-38G-R6_bake_report.md`
- `target/16AI-QW-38G-R6_static_validation.json`

## Implemented
- `ASH_SHADER_DEBUG_BUFFER` env-gated shader debug buffer candidate path.
- Scalar-only policy and full-vector rejection.
- Byte-budget planning and fail-closed summary/receipt.
- Live PowerShell runner for release `infer_only.exe`.
- Explicit unavailable receipt when no intermediate shader insertion point is exposed.

## Not Implemented by Design
- No full hidden vector dump.
- No weight/tokenizer/safetensors/banlist mutation.
- No shader result mutation.
- No false positive `post_mlp` / `post_block` tap success.

## Validation
- Static validation: PASS_STATIC
- Cargo check: NOT_RUN_CONTAINER_CARGO_UNAVAILABLE
