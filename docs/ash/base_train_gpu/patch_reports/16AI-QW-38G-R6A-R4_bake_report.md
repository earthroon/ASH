# 16AI-QW-38G-R6A-R4 Bake Report

## Patch
`16AI-QW-38G-R6A-R4 — Backend Extension Apply Dry-run / Pipeline Variant Candidate Seal`

## Base
`ash_pass3_16AI-QW-38G-R6A-R3_backend_debug_binding_spec_baked.zip`

## Implemented
- Added `ASH_BACKEND_EXTENSION_DRY_RUN` env-gated dry-run closure.
- Added spec loading from `workspace/qw38g_r6a_r3_backend_debug_binding_extension_spec.json`.
- Added candidate JSON for:
  - debug shader variant
  - pipeline cache key separation
  - bind group layout variant
  - debug buffer binding
  - mutation guard
- Added hard reject path for `ASH_BACKEND_EXTENSION_APPLY=1`.
- Added no-apply safeguards: no shader write, no layout mutation, no bind group mutation, no generation mutation.
- Added PowerShell runner using UTF-8 text-file input to avoid PowerShell/cmd quoting corruption.

## Files Changed
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38G_R6A_R4_backend_extension_dry_run.ps1`
- `acceptance_reports/16AI-QW-38G-R6A-R4_backend_extension_apply_dry_run.md`
- `patch_reports/16AI-QW-38G-R6A-R4_native_wgpu.diff`

## Validation
- Static validation: PASS_STATIC
- Cargo check in container: NOT_RUN_CONTAINER_CARGO_UNAVAILABLE

## Runtime Outputs
Expected after local run:
- `workspace/qw38g_r6a_r4_backend_extension_dry_run.json`
- `workspace/qw38g_r6a_r4_backend_extension_dry_run_receipt.json`
- `workspace/infer_qw38g_r6a_r4_backend_extension_dry_run_live.log`
