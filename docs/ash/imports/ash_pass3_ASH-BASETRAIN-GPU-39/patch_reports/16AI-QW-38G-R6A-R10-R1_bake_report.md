# 16AI-QW-38G-R6A-R10-R1 Bake Report

## Patch
`16AI-QW-38G-R6A-R10-R1 — Multi-Seed Final Boundary Aggregation / Repro Confidence Lift Seal`

## Base
`ash_pass3_16AI-QW-38G-R6A-R11-R1_projection_margin_reachability_baked.zip`

## Static Validation
`PASS_STATIC`

## Cargo Check
`NOT_RUN_CONTAINER_CARGO_UNAVAILABLE`

## Files Changed
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38G_R6A_R10_R1_multiseed_aggregation.ps1`
- `acceptance_reports/16AI-QW-38G-R6A-R10-R1_multiseed_final_boundary_aggregation.md`
- `patch_reports/16AI-QW-38G-R6A-R10-R1_native_wgpu.diff`
- `patch_reports/16AI-QW-38G-R6A-R10-R1_runner.diff`
- `target/16AI-QW-38G-R6A-R10-R1_static_validation.json`

## Implemented Behavior
- Adds multi-seed aggregation receipt generation.
- Supports aggregate-only and runner-assisted fanout modes.
- Ensures each seed is a separate `infer_only.exe` run in fanout mode.
- Preserves seed-specific R10/R11 artifacts without overwriting the default files.
- Produces `PASS`, `PARTIAL`, or `FAIL` aggregation status based on actual seed evidence.

## Guard Rails
- Production apply is hard-rejected.
- Full vector readback is hard-rejected.
- Seed count is limited.
- Target count is limited.
- Missing seed receipts are recorded as incomplete evidence, not silently ignored.
