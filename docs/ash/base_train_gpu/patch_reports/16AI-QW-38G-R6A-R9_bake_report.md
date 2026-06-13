# 16AI-QW-38G-R6A-R9 Bake Report

## Patch
`16AI-QW-38G-R6A-R9 — Scalar Tap Layer/Stage Compare / Reserved Direction Source Probe Seal`

## Base
`ash_pass3_16AI-QW-38G-R6A-R8_debug_buffer_scalar_readback_baked.zip`

## Files Modified
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38G_R6A_R9_scalar_tap_compare.ps1`

## Files Added
- `acceptance_reports/16AI-QW-38G-R6A-R9_scalar_tap_layer_stage_compare.md`
- `patch_reports/16AI-QW-38G-R6A-R9_bake_report.md`
- `patch_reports/16AI-QW-38G-R6A-R9_native_wgpu.diff`
- `target/16AI-QW-38G-R6A-R9_static_validation.json`

## Runtime Behavior
Adds an env-gated R9 compare probe:
- `ASH_SCALAR_TAP_COMPARE=1`
- `ASH_SCALAR_TAP_COMPARE_MODE=layer_stage_probe`
- validates R8 source receipt/summary/trace
- emits layer/stage compare trace, summary, receipt, rollback receipt
- enforces scalar-only and production-apply rejection

## SSOT Boundary
R9 does not claim unavailable intermediate activations as captured. Current available scalar boundary is `last/post_final_norm` from R8 projection-boundary scalar readback. Other requested stage records are explicitly marked unavailable if the current sandbox does not expose them.

## Validation
Static checks only. Cargo is unavailable in the bake container.
