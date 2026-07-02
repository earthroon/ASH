# ASH-BASETRAIN-GPU-70K-G211B26-R1

## Promotion Candidate Review Source Receipt Unwrap Fix

PatchId: `ASH-BASETRAIN-GPU-70K-G211B26-R1`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G211B26`  
SourceRuntimePatchId: `ASH-BASETRAIN-GPU-70K-G211B25`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G211B27`  
PatchKind: `RuntimeSourceLoaderHotfix`  
Phase: `PhaseTensorCubeGpuControlledPromotionCandidateReviewSourceReceiptUnwrapFix`

RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G211B26_TENSORCUBE_GPU_CONTROLLED_PROMOTION_CANDIDATE_REVIEW_GATE_REVIEW_PREPARED_CONTROLLED_PROMOTION_CANDIDATE_BEFORE_PRODUCTION_PROMOTION_GATE_NO_SILENT_FALLBACK_NO_PRODUCTION_WEIGHT_MUTATION_NO_TENSORCORE_CLAIM`

HotfixPassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G211B26_R1_PROMOTION_CANDIDATE_REVIEW_SOURCE_RECEIPT_UNWRAP_FIX_UNWRAP_G211B25_ROOT_RECEIPT_OBJECT_BEFORE_SOURCE_VALIDATION_NO_STATE_CHANGE_NO_PRODUCTION_MUTATION_NO_TENSORCORE_CLAIM`

## Purpose

G211B26-R1 fixes the G211B26 source loader used by the promotion candidate review gate.

G211B26 failed with `Error: G211B26 source G211B25 promotion candidate prepare state rejected` because G211B25 writes runtime artifacts with a root wrapper containing `schema` and nested `receipt`, while G211B26 expected source validation fields directly at the root object.

G211B26-R1 updates the source loader to unwrap the root `receipt` object before source validation. It does not change G211B26 state semantics, does not change G211B25 artifacts, does not weaken source validation, does not bypass missing file checks, and does not silently fallback to alternate routes.

G211B26-R1 does not approve, apply, or promote the promotion candidate. It does not execute production promotion, mutate production weights, write persistent storage, create checkpoint or safetensors snapshots, rewrite checkpoint or safetensors files, persist rollback anchor, execute rollback, create a new command encoder, submit a new command buffer, execute a new compute dispatch, or claim TensorCore hardware acceleration.

## Target Runtime File

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211b26_tensorcube_gpu_controlled_promotion_candidate_review_gate.rs
```

Runtime binary remains unchanged:

```text
ash_basetrain_gpu_70k_g211b26_tensorcube_gpu_controlled_promotion_candidate_review_gate
```

Cargo command remains unchanged:

```bash
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211b26_tensorcube_gpu_controlled_promotion_candidate_review_gate
```

## Core Fix

Required helper behavior:

```text
1. Read source artifact JSON.
2. Parse JSON as serde_json::Value.
3. Require root JSON to be an object.
4. If root contains receipt object, return cloned receipt map.
5. If root does not contain receipt object, return root map.
6. Do not synthesize missing fields.
7. Do not inject default source acceptance values.
8. Do not allow silent fallback.
```

Required implementation shape:

```rust
fn load_receipt(source_dir: &Path, name: &str) -> Result<Map<String, Value>> {
    let path = source_dir.join(name);
    let text = fs::read_to_string(&path)?;
    let value: Value = serde_json::from_str(&text)?;

    match value {
        Value::Object(root) => match root.get("receipt") {
            Some(Value::Object(receipt)) => Ok(receipt.clone()),
            _ => Ok(root),
        },
        _ => bail!("receipt is not object: {}", path.display()),
    }
}
```

Rejected implementation:

```text
load_receipt returns root object while receipt object exists
load_receipt silently creates empty map
load_receipt injects promotion_candidate_prepare_executed=true
load_receipt injects promotion_candidate_prepare_status=Prepared
load_receipt bypasses source_accepted validation
load_receipt ignores JSON parse failure
load_receipt ignores missing file failure
load_receipt falls back to G211B24 artifacts
load_receipt falls back to production/checkpoint/safetensors route
```

## Source Validation Contract

G211B26-R1 must preserve the original G211B26 source validation contract. After receipt unwrap, G211B26 must still validate that G211B25 PASS marker is present, promotion candidate prepare/descriptor/result/receipt/prepared-state/source-chain/review-gate-ready states are valid, and all apply/promotion/production/storage/TensorCore boundaries remain false.

Critical accepted source states remain:

```text
source_patch_id=ASH-BASETRAIN-GPU-70K-G211B25
source_g211b25_pass_marker_status=Present
source_promotion_candidate_prepare_executed=true
source_promotion_candidate_prepared=true
source_promotion_candidate_prepare_status=PreparedOrPreparedWithWarning
source_promotion_candidate_descriptor_status=Created
source_promotion_candidate_descriptor_scope=DescriptorOnlyNoApplyNoProductionMutation
source_promotion_candidate_descriptor_route=TensorCubeGpuExecutionPath
source_promotion_candidate_descriptor_production_visible=false
source_promotion_candidate_descriptor_apply_enabled=false
source_promotion_candidate_descriptor_weight_write_enabled=false
source_promotion_candidate_prepare_result_status=PromotionCandidatePrepared
source_promotion_candidate_prepare_receipt_status=Created
source_promotion_candidate_prepared_state_status=ReadyForPromotionCandidateReview
source_promotion_candidate_source_chain_status=Valid
source_promotion_candidate_source_route=TensorCubeGpuExecutionPath
source_promotion_candidate_review_gate_ready=true
source_promotion_candidate_review_gate_ready_status=Ready
source_promotion_candidate_approved=false
source_promotion_candidate_applied=false
source_promotion_candidate_promoted=false
source_promotion_candidate_apply_allowed=false
source_promotion_candidate_production_visible=false
source_promotion_candidate_weight_write_allowed=false
source_production_promotion_ready=false
source_production_promotion_executed=false
source_production_weight_mutation_allowed=false
source_persistent_storage_write_allowed=false
source_rollback_execution_allowed=false
source_new_compute_dispatch_performed=false
source_new_runtime_execution_receipt_created=false
source_tensorcore_hardware_acceleration_claimed=false
source_ready_for_g211b26=true
```

## No State Change Contract

```text
state_semantics_changed=false
receipt_semantics_changed=false
json_key_schema_changed=false
artifact_path_schema_changed=false
source_validation_rules_weakened=false
source_validation_bypass_added=false
promotion_candidate_review_semantics_changed=false
production_promotion_gate_semantics_changed=false
pass_marker_changed=false
runtime_binary_changed=false
cargo_command_changed=false
next_patch_changed=false
source_receipt_loader_unwraps_root_receipt_object=true
source_receipt_loader_flat_root_fallback_preserved=true
```

Forbidden state changes remain false:

```text
promotion_candidate_approval_allowed=false
promotion_candidate_apply_allowed=false
production_promotion_execution_allowed=false
production_promotion_ready_allowed=false
production_replacement_allowed=false
production_weight_mutation_allowed=false
persistent_storage_write_allowed=false
rollback_anchor_persistent_write_allowed=false
rollback_execution_allowed=false
checkpoint_snapshot_allowed=false
safetensors_snapshot_allowed=false
production_route_snapshot_allowed=false
new_runtime_dispatch_allowed=false
actual_command_encoder_creation_allowed=false
actual_command_buffer_submit_allowed=false
actual_compute_dispatch_allowed=false
runtime_execution_receipt_creation_allowed=false
checkpoint_rewrite_allowed=false
safetensors_rewrite_allowed=false
weight_write_allowed=false
optimizer_state_mutation_allowed=false
training_weight_mutation_allowed=false
benchmark_claim_allowed=false
tensorcore_hardware_acceleration_claim_allowed=false
```

## Static Surface Requirements

```text
runtime_outputs_prebaked=0
target_runtime_file_present=true
load_receipt_function_present=true
load_receipt_reads_json_file=true
load_receipt_parses_serde_json_value=true
load_receipt_requires_root_object=true
load_receipt_unwraps_receipt_object=true
load_receipt_returns_receipt_clone=true
load_receipt_flat_root_fallback_preserved=true
load_receipt_empty_map_fallback_absent=true
load_receipt_source_default_injection_absent=true
load_receipt_source_validation_bypass_absent=true
source_validation_rules_preserved=true
source_accepted_gate_preserved=true
source_rejection_error_preserved=true
ps1_files_included=0
py_files_included=0
sha256_files_included=0
verdict=PASS_STATIC_SURFACE
```

## Acceptance Criteria

```text
1. G211B26 runtime compiles.
2. load_receipt unwraps root.receipt object when present.
3. load_receipt preserves flat root object fallback when receipt object is absent.
4. load_receipt does not synthesize source fields.
5. load_receipt does not bypass source validation.
6. G211B25 PASS marker is loaded.
7. G211B25 promotion candidate prepare receipt is loaded through unwrapped receipt map.
8. source_accepted=true only after original G211B26 source validation passes.
9. promotion_candidate_prepare_reviewed=true.
10. promotion_candidate_descriptor_reviewed=true.
11. promotion_candidate_prepared_state_reviewed=true.
12. promotion_candidate_source_chain_reviewed=true.
13. production_promotion_gate_ready=true.
14. production_promotion_ready=false.
15. production_promotion_executed=false.
16. promotion_candidate_approved=false.
17. promotion_candidate_applied=false.
18. promotion_candidate_promoted=false.
19. production_weight_mutation_allowed=false.
20. persistent_storage_write_allowed=false.
21. tensorcore_hardware_acceleration_claimed=false.
22. ready_for_g211b27=true.
23. Original G211B26 PASS marker is emitted.
```

## Rejection Criteria

```text
load_receipt returns root while root.receipt is object
load_receipt creates empty source map for valid wrapped receipt
load_receipt injects source_promotion_candidate_prepare_executed=true
load_receipt injects source_promotion_candidate_prepare_status=Prepared
source_validation_rules_weakened=true
source_validation_bypass_added=true
source_accepted=true while required G211B25 source fields are missing
source_accepted=true while required G211B25 source fields are false or empty
source_accepted=true while production mutation fields are true
source_accepted=true while promotion candidate apply fields are true
PASS marker emitted while source_accepted=false
PASS marker emitted while production_promotion_executed=true
PASS marker emitted while production_weight_mutation_allowed=true
PASS marker emitted while persistent_storage_write_allowed=true
```

## Expected Runtime Artifacts

G211B26-R1 keeps the original G211B26 runtime artifact contract. Rust must create runtime artifacts locally. No G211B26 or G211B26-R1 runtime artifacts should be prebaked into the ZIP.

Optional hotfix receipt, if emitted, must be local runtime output only and must not be prebaked into the ZIP:

```text
artifacts/g211b26/ASH_BASETRAIN_GPU_70K_G211B26_R1_SOURCE_RECEIPT_UNWRAP_FIX_RECEIPT.json
```

## Suggested Files For Bake

```text
specs/ASH_BASETRAIN_GPU_70K_G211B26_R1_SPEC.md
specs/ASH_BASETRAIN_GPU_70K_G211B26_R1_STATIC_CHECKS.json
specs/ASH_BASETRAIN_GPU_70K_G211B26_R1_LOCAL_BAKE_VALIDATION.json
specs/ASH_BASETRAIN_GPU_70K_G211B26_R1_BAKE_MANIFEST.json
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211b26_tensorcube_gpu_controlled_promotion_candidate_review_gate.rs
```

## PASS Marker

Original G211B26 runtime PASS marker must remain:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211B26_TENSORCUBE_GPU_CONTROLLED_PROMOTION_CANDIDATE_REVIEW_GATE_REVIEW_PREPARED_CONTROLLED_PROMOTION_CANDIDATE_BEFORE_PRODUCTION_PROMOTION_GATE_NO_SILENT_FALLBACK_NO_PRODUCTION_WEIGHT_MUTATION_NO_TENSORCORE_CLAIM
```

Optional hotfix receipt marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211B26_R1_PROMOTION_CANDIDATE_REVIEW_SOURCE_RECEIPT_UNWRAP_FIX_UNWRAP_G211B25_ROOT_RECEIPT_OBJECT_BEFORE_SOURCE_VALIDATION_NO_STATE_CHANGE_NO_PRODUCTION_MUTATION_NO_TENSORCORE_CLAIM
```

## Next Patch

After G211B26-R1 passes, continue to `ASH-BASETRAIN-GPU-70K-G211B27`.

```text
TensorCube GPU Controlled Production Promotion Gate Open /
Open Controlled Production Promotion Gate From Reviewed Promotion Candidate /
No Silent Fallback No Production Weight Mutation No TensorCore Claim
```
