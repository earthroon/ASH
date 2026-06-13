# 16AI-QW-38G-R6A-R7 Bake Report

## Patch
`16AI-QW-38G-R6A-R7 — Backend Extension Apply Sandbox / Debug Variant Smoke Seal`

## Base
`ash_pass3_16AI-QW-38G-R6A-R6_apply_candidate_baked.zip`

## Summary
Added a sandbox-only debug variant smoke gate after the R6 guarded apply candidate. The patch consumes the R6 apply candidate and receipt, validates the mutation guard and rollback plan, then builds sandbox smoke JSON for shader variant/cache key/bind group layout/debug buffer binding candidates without production apply or readback.

## Files changed
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38G_R6A_R7_sandbox_smoke.ps1`
- `acceptance_reports/16AI-QW-38G-R6A-R7_backend_extension_apply_sandbox.md`
- `patch_reports/16AI-QW-38G-R6A-R7_native_wgpu.diff`
- `patch_reports/16AI-QW-38G-R6A-R7_runner.diff`
- `target/16AI-QW-38G-R6A-R7_static_validation.json`

## Safety
- Production apply is hard rejected in R7.
- Readback is hard rejected in R7.
- Full vector readback is hard rejected.
- Sandbox smoke writes receipt and rollback receipt.
- Normal path guard remains explicit.

## Validation
- Static validation: PASS_STATIC
- Cargo check/build in container: NOT_RUN_CONTAINER_CARGO_UNAVAILABLE
