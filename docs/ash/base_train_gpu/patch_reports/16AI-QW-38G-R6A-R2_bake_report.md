# 16AI-QW-38G-R6A-R2 Bake Report

## Patch
**16AI-QW-38G-R6A-R2 — Burn WGPU Pipeline Layout Owner Audit / Backend Boundary Seal**

## Base
`ash_pass3_16AI-QW-38G-R6A-R1_pipeline_layout_audit_baked.zip`

## Files changed
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38G_R6A_R2_burn_wgpu_owner_audit.ps1`
- `acceptance_reports/16AI-QW-38G-R6A-R2_burn_wgpu_pipeline_layout_owner_audit.md`
- `patch_reports/16AI-QW-38G-R6A-R2_native_wgpu.diff`
- `patch_reports/16AI-QW-38G-R6A-R2_runner.ps1.snapshot`
- `target/16AI-QW-38G-R6A-R2_static_validation.json`

## Implementation
Added a dry-run backend owner audit gated by:

```txt
ASH_BURN_WGPU_OWNER_AUDIT=1
ASH_BURN_WGPU_OWNER_AUDIT_VERBOSE=1
ASH_BURN_WGPU_OWNER_AUDIT_DRY_RUN=1
ASH_BURN_WGPU_OWNER_AUDIT_OUT=workspace/qw38g_r6a_r2_burn_wgpu_owner_audit.json
ASH_BURN_WGPU_OWNER_AUDIT_RECEIPT=workspace/qw38g_r6a_r2_runtime_receipt.json
```

The audit records owner candidates for:
- Burn/WGPU dependency boundary
- shader source owner
- shader module owner
- compute pipeline owner
- pipeline layout owner
- bind group layout owner
- bind group owner
- pipeline cache key owner
- kernel dispatch owner

## Runtime behavior
The R2 audit is called from the vocab-atlas projection hot path after R6A/R6A-R1 audit hooks.

Expected primary status:

```txt
PASS_BACKEND_OWNER_AUDIT_BACKEND_PATCH_REQUIRED
```

Expected next patch:

```txt
16AI-QW-38G-R6A-R3_BACKEND_DEBUG_BINDING_EXTENSION_SPEC
```

## Static validation
`PASS_STATIC`

## Cargo check
`NOT_RUN_CONTAINER_CARGO_UNAVAILABLE`

The container does not have `cargo`, so compilation must be verified locally.
