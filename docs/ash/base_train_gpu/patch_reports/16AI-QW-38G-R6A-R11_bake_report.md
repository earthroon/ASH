# 16AI-QW-38G-R6A-R11 Bake Report

## Patch
`16AI-QW-38G-R6A-R11 — Projection Boundary Margin Audit / Masked Top1 Compare Seal`

## Base
`ash_pass3_16AI-QW-38G-R6A-R10_final_boundary_confirm_baked.zip`

## Files Changed
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38G_R6A_R11_projection_margin_audit.ps1`
- `acceptance_reports/16AI-QW-38G-R6A-R11_projection_boundary_margin_audit.md`
- `patch_reports/16AI-QW-38G-R6A-R11_bake_report.md`
- `patch_reports/16AI-QW-38G-R6A-R11_native_wgpu.diff`
- `patch_reports/16AI-QW-38G-R6A-R11_runner.diff`
- `target/16AI-QW-38G-R6A-R11_static_validation.json`

## Static Validation
`PASS_STATIC`

## Cargo Check
`NOT_RUN_CONTAINER_CARGO_UNAVAILABLE`

## Runtime Intent
R11 audits the projection boundary margin between raw top1 reserved `token_id=13` and the masked top1 candidate. It does not claim root cause and does not mutate production backend state.

## Mutation Guard
- `production_apply` rejected.
- `full_vector_readback` rejected.
- Normal path guard remains explicit in summary/receipt.
- Rollback receipt is always written on success/failure path.

## Expected Success Receipt
`status = PASS_PROJECTION_MARGIN_AUDIT`

Expected fields:
- `projection_margin_confirmed`
- `projection_margin_strength`
- `candidate_confidence_after_margin`
- `raw_top1_target_rate`
- `ban_mask_displacement_rate`
- `min_target_margin_vs_masked_top1`
- `normal_path_guard_passed`
- `rollback_receipt_written`
