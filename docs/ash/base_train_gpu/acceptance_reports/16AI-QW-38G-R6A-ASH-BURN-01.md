# 16AI-QW-38G-R6A-ASH-BURN-01

## Burn Backend Vendor Scaffold Inventory / No Backend Route Promotion Seal

## SSOT

```txt
Burn backend/vendor scaffold is inventory-only.
Backend route promotion, feature activation, raw bridge promotion, executor replacement, runtime mutation, and output emission are forbidden.
```

## Confirmed inventory evidence

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

## PASS

```txt
PASS_ASH_BURN_01_BACKEND_VENDOR_SCAFFOLD_INVENTORY_NO_BACKEND_ROUTE_PROMOTION
```

Required:

```txt
burn00_baseline_respected = true
burn_webgpu_backend_crate_present = true
vendor_fork_scaffold_present = true
burn_raw_access_local_feature_declared = true
burn_raw_access_local_default_enabled = false
burn_wgpu_local_optional_dependency = true
burn_fusion_local_optional_dependency = true
raw_bridge_uses_wgpu26_alias = true
wgpu_generation_mismatch_risk_detected = true
same_device_bridge_generation_alignment_required = true
raw_bridge_module_present = true
existing_device_bootstrap_module_present = true
same_device_borrow_path_present = true
host_upload_fallback_path_present = true
strict_raw_bridge_fail_path_present = true
upstream_real_insert_manifest_present = true
build_verified_upstream_fork_claimed = false
backend_route_policy_inventory_created = true
feature_activation_performed = false
backend_route_promotion_executed = false
active_backend_pointer_mutated = false
production_default_changed = false
executor_replaced = false
forward_execution_triggered = false
tensor_buffer_written = false
runtime_sequence_mutated = false
production_output_emitted = false
```

## WARN

```txt
WARN_ASH_BURN_01_WGPU_GENERATION_MISMATCH_REQUIRES_VENDOR_ALIGNMENT
```

Allowed warning:

```txt
raw_bridge_uses_wgpu26_alias = true
burn_wgpu_local_generation_mismatch_risk_detected = true
same_device_bridge_generation_aligned = false
```

## FAIL

```txt
FAIL_BURN00_BASELINE_MISSING
FAIL_BURN_WEBGPU_BACKEND_CRATE_MISSING
FAIL_VENDOR_FORK_SCAFFOLD_MISSING
FAIL_BURN_RAW_ACCESS_LOCAL_FEATURE_MISSING
FAIL_VENDOR_FEATURE_DEFAULT_ENABLED_TOO_EARLY
FAIL_VENDOR_DEPENDENCY_PROMOTED_TO_REQUIRED_RUNTIME
FAIL_WGPU_GENERATION_BOUNDARY_NOT_RECORDED
FAIL_SAME_DEVICE_BRIDGE_PROMOTED_WITH_GENERATION_MISMATCH
FAIL_VENDOR_FEATURE_ACTIVATED_TOO_EARLY
FAIL_EXISTING_DEVICE_BOOTSTRAP_EXECUTED_TOO_EARLY
FAIL_BACKEND_ROUTE_PROMOTED_TOO_EARLY
FAIL_ACTIVE_BACKEND_POINTER_MUTATED_TOO_EARLY
FAIL_PRODUCTION_DEFAULT_CHANGED_TOO_EARLY
FAIL_UPSTREAM_REAL_INSERT_APPLIED_TOO_EARLY
FAIL_UPSTREAM_MIRROR_CLAIMED_AS_BUILD_VERIFIED_FORK
FAIL_EXECUTOR_REPLACED_TOO_EARLY
FAIL_BACKEND_ROUTE_CHANGED_TOO_EARLY
FAIL_FORWARD_EXECUTION_TRIGGERED_TOO_EARLY
FAIL_TENSOR_DATA_MATERIALIZED_TOO_EARLY
FAIL_TENSOR_VALUE_MUTATED_TOO_EARLY
FAIL_TENSOR_BUFFER_WRITTEN_TOO_EARLY
FAIL_RUNTIME_APPLY_EXECUTED_TOO_EARLY
FAIL_RUNTIME_SEQUENCE_MUTATED_TOO_EARLY
FAIL_RUNTIME_TOKEN_APPEND_EXECUTED_TOO_EARLY
FAIL_PRODUCTION_OUTPUT_EMITTED_TOO_EARLY
FAIL_FINAL_RESPONSE_EMITTED_TOO_EARLY
FAIL_ASH_BURN01_RECEIPT_DIGEST_MISMATCH
FAIL_ASH_BURN01_RECEIPT_KEY_MISMATCH
```

## Positive cases

```txt
CASE-POS-ASH-BURN-01-00
Burn backend crate + vendor scaffold + feature gate inventory present
backend route promotion false
→ PASS

CASE-POS-ASH-BURN-01-01
burn-raw-access-local declared but default-off
vendor deps optional
→ PASS

CASE-POS-ASH-BURN-01-02
wgpu20 + wgpu26 boundary recorded
same-device bridge alignment required
no bridge promotion
→ PASS or WARN

CASE-POS-ASH-BURN-01-03
QWave backend route policy files inventoried
active backend pointer not mutated
→ PASS
```

## Negative cases

```txt
CASE-NEG-ASH-BURN-01-00
backend route promotion executed
→ FAIL_BACKEND_ROUTE_PROMOTED_TOO_EARLY

CASE-NEG-ASH-BURN-01-01
burn-raw-access-local default enabled
→ FAIL_VENDOR_FEATURE_DEFAULT_ENABLED_TOO_EARLY

CASE-NEG-ASH-BURN-01-02
existing device bootstrap executed
→ FAIL_EXISTING_DEVICE_BOOTSTRAP_EXECUTED_TOO_EARLY

CASE-NEG-ASH-BURN-01-03
tensor buffer written
→ FAIL_TENSOR_BUFFER_WRITTEN_TOO_EARLY

CASE-NEG-ASH-BURN-01-04
production output emitted
→ FAIL_PRODUCTION_OUTPUT_EMITTED_TOO_EARLY
```
