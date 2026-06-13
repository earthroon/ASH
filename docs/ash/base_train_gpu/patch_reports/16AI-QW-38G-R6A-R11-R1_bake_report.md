# 16AI-QW-38G-R6A-R11-R1 Bake Report

## Summary
Baked `Projection Margin Hook Reachability / Receipt Fallback Seal` on top of R11 projection margin audit.

## Modified Files
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38G_R6A_R11_R1_projection_margin_reachability.ps1`
- `acceptance_reports/16AI-QW-38G-R6A-R11-R1_projection_margin_hook_reachability.md`
- `patch_reports/16AI-QW-38G-R6A-R11-R1_native_wgpu.diff`
- `patch_reports/16AI-QW-38G-R6A-R11-R1_runner.diff`
- `target/16AI-QW-38G-R6A-R11-R1_static_validation.json`

## Static Validation
`PASS_STATIC`

## Cargo
`NOT_RUN_CONTAINER_CARGO_UNAVAILABLE`

## Notes
This patch does not claim projection margin success by itself. It guarantees that R11 no longer finishes with missing receipt/summary/trace silently. If the hook is not reached, R11-R1 writes a failure receipt and reachability JSON.
