# 16AI-QW-38G-R6A-ASH-BURN-01 Bake Report

## Title

Burn Backend Vendor Scaffold Inventory / No Backend Route Promotion Seal

## Source SSOT

```txt
Base artifact: ash_pass3_ASH-BURN-00_runtime_internal_baseline_probe_baked.zip
Branch: ASH-BURN backend/vendor scaffold inventory
Mode: read-only backend/vendor route boundary evidence
```

## Implemented files

```txt
crates/ash_core/src/ash_burn_01_backend_vendor_scaffold_inventory.rs
crates/ash_core/src/bin/ash_burn_01_backend_vendor_scaffold_inventory.rs
crates/ash_core/src/lib.rs
acceptance_reports/16AI-QW-38G-R6A-ASH-BURN-01.md
patch_reports/16AI-QW-38G-R6A-ASH-BURN-01_bake_report.md
ASH_BURN_01_STATIC_CHECKS.txt
ASH_BURN_01_BAKE_MANIFEST.json
```

## Confirmed backend/vendor evidence

```json
{
  "backend_crate_present": true,
  "backend_crate_file_count": 277,
  "backend_spec_present": true,
  "backend_spec_full_train_present": true,
  "vendor_fork_scaffold_present": true,
  "vendor_scaffold_file_count": 29,
  "burn_wgpu_local_scaffold_present": true,
  "burn_fusion_local_scaffold_present": true,
  "upstream_real_insert_manifest_present": true,
  "burn_raw_access_local_feature_declared": true,
  "burn_raw_access_local_default_enabled": false,
  "burn_wgpu_local_optional_dependency": true,
  "burn_fusion_local_optional_dependency": true,
  "raw_bridge_uses_wgpu26_alias": true,
  "wgpu_generation_mismatch_risk_detected": true,
  "same_device_borrow_path_present": true,
  "host_upload_fallback_path_present": true,
  "strict_raw_bridge_fail_path_present": true,
  "qwave_backend_policy_files_present": {
    "crates/burn_webgpu_backend/src/qwave_atlas_backend_router.rs": true,
    "crates/burn_webgpu_backend/src/qwave_backend_switch_dryrun.rs": true,
    "crates/burn_webgpu_backend/src/qwave_backend_apply_candidate.rs": true,
    "crates/burn_webgpu_backend/src/qwave_backend_apply_sandbox.rs": true,
    "crates/burn_webgpu_backend/src/qwave_backend_rollback_ledger.rs": true,
    "crates/burn_webgpu_backend/src/qwave_backend_recovery_candidate.rs": true,
    "crates/burn_webgpu_backend/src/qwave_backend_apply_preflight.rs": true,
    "crates/burn_webgpu_backend/src/qwave_backend_shadow_commit.rs": true
  }
}
```

## Seal

```txt
burn_raw_access_local_feature_declared = true
burn_raw_access_local_default_enabled = false
raw_bridge_uses_wgpu26_alias = true
wgpu_generation_mismatch_risk_detected = true
backend_route_promotion_executed = false
feature_activation_performed = false
existing_device_bootstrap_executed = false
executor_replaced = false
tensor_buffer_written = false
runtime_sequence_mutated = false
production_output_emitted = false
```
