# 16AI-QW-38G-R4 Bake Report

## Patch
16AI-QW-38G-R4 — GPU Debug Tap Candidate / Bounded Intermediate Activation Readback Seal

## Base
`ash_pass3_16AI-QW-38G-R3_stage_map_baked.zip`

## Files Changed
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38G_R4_gpu_debug_tap.ps1`
- `acceptance_reports/16AI-QW-38G-R4_gpu_debug_tap_candidate.md`
- `patch_reports/16AI-QW-38G-R4_bake_report.md`
- `patch_reports/16AI-QW-38G-R4_native_wgpu.diff`
- `patch_reports/16AI-QW-38G-R4_runner.diff`
- `target/16AI-QW-38G-R4_static_validation.json`

## Implementation Summary
- Added `ASH_GPU_DEBUG_TAP` gated debug-tap candidate surface.
- Added bounded defaults: `max_steps=1`, `layers=mid,last`, `stages=post_mlp,post_block`, `target_ids=13`, `scalar_only=true`.
- Added fail-closed summary and receipt writer:
  - `workspace/qw38g_r4_gpu_debug_tap_summary.json`
  - `workspace/qw38g_r4_gpu_debug_tap_receipt.json`
- Added optional final-boundary fallback only when `post_final_norm` or `final_hidden_projection` is explicitly requested.
- Does not mutate weights, tokenizer, safetensors, banlist, prompt template, or LoRA.

## Runtime Philosophy
R3 proved current Rust-side boundary reaches final hidden projection but not layerwise residual. R4 therefore treats `post_mlp/post_block` as a candidate GPU tap and reports unavailability honestly when the stage is not reachable.

## Validation
- Static validation: `PASS_STATIC`
- Cargo validation in container: `NOT_RUN_CONTAINER_CARGO_UNAVAILABLE`

## Expected First Run
```powershell
.\scripts\run_16AI_QW_38G_R4_gpu_debug_tap.ps1 -Build
```

Then inspect:
```powershell
Get-Content ".\workspace\qw38g_r4_gpu_debug_tap_receipt.json" -Encoding UTF8
Get-Content ".\workspace\qw38g_r4_gpu_debug_tap_summary.json" -Encoding UTF8
```
