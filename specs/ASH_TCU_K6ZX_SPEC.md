# ASH-TCU-K6ZX SPEC

## Title

Rollback Rehearsal And Apply Dryrun / Apply Queue Candidate To Non-Committing Runtime Splice Rehearsal / Shadow Route Swap And Restore / No Default Adoption No Production Replacement Seal

## Patch ID

```txt
ASH-TCU-K6ZX
```

## Status Target

```txt
PASS_ASH_TCU_K6ZX_ROLLBACK_REHEARSAL_AND_APPLY_DRYRUN_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K6ZW
```

## Required Prior Status

```txt
PASS_ASH_TCU_K6ZW_APPLY_QUEUE_ENTRY_OPERATOR_GATE_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
apply_queue_entry_created_pending_operator_review_no_default_adoption
```

## Purpose

`ASH-TCU-K6ZX` uses the K6ZW apply queue candidate as the required parent state and performs a non-committing apply dryrun plus rollback rehearsal.

K6ZW created the apply queue candidate and bound rollback metadata, but did not execute apply, runtime splice, default adoption, production replacement, or user-visible adoption.

K6ZX is the first patch in this chain allowed to execute a dryrun-only runtime splice rehearsal.

K6ZX may perform a shadow route swap inside an isolated rehearsal namespace.

K6ZX must restore the previous route inside that rehearsal namespace.

K6ZX must prove that rollback can restore the previous route after a dryrun swap.

K6ZX does not perform real apply, open production route replacement, mutate default route registry, or expose user-visible output.

K6ZX does not bind base_train, weight atlas, GPU streaming, loss/backward, optimizer, weight commit, safetensors mutation, or checkpoint finalization.

## Current K6ZW Baseline

K6ZW established:

```txt
apply_queue_candidate_created = true
apply_queue_entry_created = true
apply_queue_ready = true
apply_queue_state = pending_operator_review
operator_gate_required = true
operator_gate_state = pending
operator_approval_granted = false
apply_execution_started = false
apply_execution_completed = false
runtime_splice_opened = false
default_adoption_executed = false
production_replacement_executed = false
user_visible_adoption_executed = false
rollback_plan_bound = true
rollback_rehearsal_required_next = true
recommended_next_patch = ASH-TCU-K6ZX_ROLLBACK_REHEARSAL_AND_APPLY_DRYRUN_NO_DEFAULT_ADOPTION
```

K6ZX must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zx_apply_dryrun_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zx_prior_k6zw_apply_queue_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_dryrun_rehearsal_namespace_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_shadow_route_snapshot_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_non_committing_runtime_splice_rehearsal_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_shadow_route_swap_rehearsal_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_rollback_rehearsal_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_post_rollback_restore_check_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_operator_gate_still_pending_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_no_default_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_no_user_visible_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_no_persistent_route_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_static_checks_latest.json
artifacts/ASH_TCU_K6ZX_LOCAL_MANIFEST.json
```

## State Ownership

### K6ZX owns

```txt
dryrun_rehearsal_namespace
shadow_route_snapshot
non_committing_runtime_splice_rehearsal
shadow_route_swap_rehearsal
rollback_rehearsal
post_rollback_restore_check
operator_gate_still_pending_guard
no_default_adoption_guard
no_production_replacement_guard
no_user_visible_adoption_guard
no_persistent_route_mutation_guard
```

### K6ZX does not own

```txt
operator approval grant
real apply execution
production runtime splice
default route adoption
production route replacement
user-visible adoption
base_train route binding
weight atlas construction
GPU streaming
training execution
loss/backward execution
optimizer step
weight commit
safetensors mutation
checkpoint finalization
```

## Source Inputs

K6ZX must read and validate the latest K6ZW receipts:

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zw_prior_k6zv_native_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_apply_candidate_descriptor_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_operator_gate_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_apply_queue_entry_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_apply_queue_non_execution_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_no_default_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_no_user_visible_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_rollback_binding_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_static_checks_latest.json
artifacts/ASH_TCU_K6ZW_LOCAL_MANIFEST.json
```

K6ZX may read K6ZV native parity metadata as evidence source only.

K6ZX must not recompute K6ZV parity.

K6ZX must not treat K6ZW apply queue readiness as operator approval.

## Candidate Route

K6ZX must preserve the K6ZW candidate descriptor:

```txt
apply_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
apply_candidate_kind = logical16_native_wgpu_tensorcube_candidate
candidate_route = ash_tcu_k6p_row_major_emit_candidate_v1
candidate_source_patch = ASH-TCU-K6ZV
candidate_apply_scope = candidate_only
operator_gate_required = true
operator_approval_granted = false
apply_execution_allowed = false
```

K6ZX must not mutate candidate route, dtype, layout, tile mode, or evidence status.

## Dryrun Rehearsal Namespace

K6ZX must create an isolated rehearsal namespace:

```txt
dryrun_namespace_id = ash_tcu_k6zx_rehearsal_namespace_v1
dryrun_namespace_created = true
dryrun_namespace_isolated = true
dryrun_namespace_persistent = false
dryrun_namespace_user_visible = false
dryrun_namespace_production_visible = false
```

The dryrun namespace must not alias:

```txt
default_route_registry
production_route_registry
user_visible_runtime_route
assistant_message_output_route
base_train_route_registry
```

## Shadow Route Snapshot

Before any dryrun swap, K6ZX must snapshot the current route state:

```txt
shadow_route_snapshot_created = true
snapshot_scope = rehearsal_namespace_only
snapshot_target_route = current_default_route
snapshot_candidate_route = ash_tcu_k6p_row_major_emit_candidate_v1
snapshot_hash_present = true
snapshot_used_for_restore = true
```

K6ZX must not snapshot or mutate the production route registry.

## Non-Committing Runtime Splice Rehearsal

K6ZX may perform a non-committing runtime splice rehearsal:

```txt
non_committing_runtime_splice_rehearsal_started = true
non_committing_runtime_splice_rehearsal_completed = true
runtime_splice_rehearsal_scope = rehearsal_namespace_only
runtime_splice_opened = false
production_runtime_splice_opened = false
persistent_runtime_splice_opened = false
```

This rehearsal may temporarily swap the route inside the dryrun namespace only.

This rehearsal must not open the real runtime splice.

## Shadow Route Swap Rehearsal

K6ZX may set:

```txt
shadow_route_swap_rehearsal_started = true
shadow_route_swap_rehearsal_completed = true
shadow_route_before = current_default_route
shadow_route_during = ash_tcu_k6p_row_major_emit_candidate_v1
shadow_route_after = current_default_route
```

only when all of the following are true:

```txt
dryrun_namespace_created = true
shadow_route_snapshot_created = true
operator_approval_granted = false
real_apply_execution_started = false
production_replacement_executed = false
default_route_registry_mutated = false
user_visible_adoption_executed = false
```

## Rollback Rehearsal

K6ZX must execute rollback rehearsal after the shadow route swap:

```txt
rollback_rehearsal_started = true
rollback_rehearsal_completed = true
rollback_rehearsal_scope = rehearsal_namespace_only
rollback_target_route = current_default_route
rollback_restored_route = current_default_route
rollback_executed_against_production = false
```

Rollback rehearsal must prove that the rehearsal namespace route can be restored to the pre-swap route.

K6ZX does not execute production rollback.

## Post-Rollback Restore Check

K6ZX must verify restoration after rollback rehearsal:

```txt
post_rollback_restore_check_passed = true
shadow_route_restored = true
default_route_registry_unchanged = true
production_route_registry_unchanged = true
user_visible_route_unchanged = true
runtime_decode_output_changed = false
assistant_message_output_changed = false
```

## Apply Dryrun Semantics

K6ZX may set:

```txt
apply_dryrun_started = true
apply_dryrun_completed = true
apply_dryrun_passed = true
```

K6ZX must not set:

```txt
apply_execution_started = true
apply_execution_completed = true
operator_approval_granted = true
runtime_splice_opened = true
default_adoption_executed = true
production_replacement_executed = true
user_visible_adoption_executed = true
```

## Operator Gate Semantics

K6ZX must preserve the operator gate from K6ZW:

```txt
operator_gate_required = true
operator_gate_state = pending
operator_approval_granted = false
operator_approval_source = none
operator_approval_signature_present = false
```

K6ZX must not infer operator approval from successful dryrun, rollback rehearsal, or absence of failures.

## Explicit Non-Scope

K6ZX does not enable:

```txt
operator approval grant
real apply execution
persistent runtime splice
production route replacement
default route adoption
user-visible output adoption
performance claim
base_train route binding
weight atlas construction
GPU streaming
loss/backward
optimizer
weight commit
safetensors mutation
checkpoint finalization
```

## Guard Requirements

### Prior K6ZW Apply Queue Guard

K6ZX must verify:

```txt
required_prior_patch = ASH-TCU-K6ZW
required_prior_pass = true
k6zw_apply_queue_candidate_created = true
k6zw_apply_queue_entry_created = true
k6zw_apply_queue_ready = true
k6zw_apply_queue_state = pending_operator_review
k6zw_operator_gate_required = true
k6zw_operator_approval_granted = false
k6zw_rollback_plan_bound = true
k6zw_rollback_rehearsal_required_next = true
```

### Dryrun Namespace Guard

K6ZX must verify:

```txt
dryrun_namespace_created = true
dryrun_namespace_isolated = true
dryrun_namespace_persistent = false
dryrun_namespace_user_visible = false
dryrun_namespace_production_visible = false
```

### Non-Committing Runtime Splice Rehearsal Guard

K6ZX must verify:

```txt
non_committing_runtime_splice_rehearsal_started = true
non_committing_runtime_splice_rehearsal_completed = true
runtime_splice_rehearsal_scope = rehearsal_namespace_only
runtime_splice_opened = false
production_runtime_splice_opened = false
persistent_runtime_splice_opened = false
```

### Rollback Rehearsal Guard

K6ZX must verify:

```txt
rollback_rehearsal_started = true
rollback_rehearsal_completed = true
rollback_rehearsal_scope = rehearsal_namespace_only
rollback_restored_route = current_default_route
rollback_executed_against_production = false
post_rollback_restore_check_passed = true
```

### No Persistent Route Mutation Guard

K6ZX must verify:

```txt
default_route_registry_mutated = false
production_route_registry_mutated = false
user_visible_route_mutated = false
base_train_route_registry_mutated = false
runtime_decode_output_changed = false
assistant_message_output_changed = false
```

### Operator Gate Still Pending Guard

K6ZX must verify:

```txt
operator_gate_required = true
operator_gate_state = pending
operator_approval_granted = false
operator_approval_signature_present = false
operator_approval_source = none
```

### No Default Adoption Guard

K6ZX must verify:

```txt
default_adoption_allowed = false
default_adoption_executed = false
global_default_route_changed = false
default_route_registry_mutated = false
```

### No Production Replacement Guard

K6ZX must verify:

```txt
production_replacement_allowed = false
production_replacement_executed = false
production_route_state_changed = false
production_route_registry_mutated = false
persistent_runtime_splice_opened = false
```

### No User-Visible Adoption Guard

K6ZX must verify:

```txt
user_visible_adoption_allowed = false
user_visible_adoption_executed = false
assistant_message_output_changed = false
runtime_decode_output_changed = false
```

### No Performance Claim Guard

K6ZX must verify:

```txt
performance_claim_allowed = false
benchmark_claim_promoted = false
apply_dryrun_promoted_to_performance_claim = false
```

K6ZX may say dryrun and rollback rehearsal passed.

K6ZX must not claim production performance superiority.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k6zx_prior_k6zw_apply_queue_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k6zx_dryrun_rehearsal_namespace.rs
crates/burn_webgpu_backend/src/tensorcube_k6zx_shadow_route_snapshot.rs
crates/burn_webgpu_backend/src/tensorcube_k6zx_non_committing_runtime_splice_rehearsal.rs
crates/burn_webgpu_backend/src/tensorcube_k6zx_shadow_route_swap_rehearsal.rs
crates/burn_webgpu_backend/src/tensorcube_k6zx_rollback_rehearsal.rs
crates/burn_webgpu_backend/src/tensorcube_k6zx_post_rollback_restore_check.rs
crates/burn_webgpu_backend/src/tensorcube_k6zx_operator_gate_still_pending_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zx_no_default_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zx_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zx_no_user_visible_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zx_no_persistent_route_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zx_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k6zx_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k6zx_rollback_rehearsal_apply_dryrun_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k6zx_rollback_rehearsal_apply_dryrun_audit.rs
```

## Test Files

```txt
crates/burn_webgpu_backend/tests/ash_tcu_k6zx_prior_k6zw_apply_queue_receipt.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zx_dryrun_rehearsal_namespace.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zx_shadow_route_snapshot.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zx_non_committing_runtime_splice_rehearsal.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zx_shadow_route_swap_rehearsal.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zx_rollback_rehearsal.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zx_post_rollback_restore_check.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zx_operator_gate_still_pending_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zx_no_default_adoption_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zx_no_production_replacement_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zx_no_user_visible_adoption_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zx_no_persistent_route_mutation_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zx_verdict.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zx_contract_audit.rs
```

## Rust Module Export Requirements

### burn_webgpu_backend lib exports

```rust
pub mod tensorcube_k6zx_prior_k6zw_apply_queue_receipt;
pub mod tensorcube_k6zx_dryrun_rehearsal_namespace;
pub mod tensorcube_k6zx_shadow_route_snapshot;
pub mod tensorcube_k6zx_non_committing_runtime_splice_rehearsal;
pub mod tensorcube_k6zx_shadow_route_swap_rehearsal;
pub mod tensorcube_k6zx_rollback_rehearsal;
pub mod tensorcube_k6zx_post_rollback_restore_check;
pub mod tensorcube_k6zx_operator_gate_still_pending_guard;
pub mod tensorcube_k6zx_no_default_adoption_guard;
pub mod tensorcube_k6zx_no_production_replacement_guard;
pub mod tensorcube_k6zx_no_user_visible_adoption_guard;
pub mod tensorcube_k6zx_no_persistent_route_mutation_guard;
pub mod tensorcube_k6zx_verdict;
pub mod tensorcube_k6zx_contract_audit;
```

### orchestrator_local lib exports

```rust
pub mod ash_tcu_k6zx_rollback_rehearsal_apply_dryrun_report;
```

## CLI

### Binary

```txt
ash_tcu_k6zx_rollback_rehearsal_apply_dryrun_audit
```

### Command

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k6zx_rollback_rehearsal_apply_dryrun_audit -- --repo-root <repo> --require-k6zw-pass --require-apply-queue-ready --require-operator-gate-pending --create-dryrun-namespace --snapshot-shadow-route --run-non-committing-splice-rehearsal --run-shadow-route-swap-rehearsal --run-rollback-rehearsal --verify-post-rollback-restore --no-persistent-route-mutation --operator-approval-granted false --no-default-adoption --no-production-replacement --no-user-visible-adoption
```

### Optional report input

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k6zx_rollback_rehearsal_apply_dryrun_audit -- --repo-root <repo> --k6zw-report-json <k6zw-report-json-or-log> --require-k6zw-pass --require-apply-queue-ready --require-operator-gate-pending --create-dryrun-namespace --snapshot-shadow-route --run-non-committing-splice-rehearsal --run-shadow-route-swap-rehearsal --run-rollback-rehearsal --verify-post-rollback-restore --no-persistent-route-mutation --operator-approval-granted false --no-default-adoption --no-production-replacement --no-user-visible-adoption
```

## Required Output JSON Shape

```json
{
  "patch_id": "ASH-TCU-K6ZX",
  "status": "PASS_ASH_TCU_K6ZX_ROLLBACK_REHEARSAL_AND_APPLY_DRYRUN_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL",
  "prior_k6zw_apply_queue_receipt": {
    "pass": true,
    "k6zw_required": true,
    "k6zw_valid": true,
    "k6zw_status": "PASS_ASH_TCU_K6ZW_APPLY_QUEUE_ENTRY_OPERATOR_GATE_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL",
    "k6zw_apply_queue_ready": true,
    "k6zw_apply_queue_state": "pending_operator_review",
    "k6zw_operator_gate_required": true,
    "k6zw_operator_approval_granted": false,
    "k6zw_rollback_plan_bound": true
  },
  "dryrun_rehearsal_namespace": {
    "pass": true,
    "dryrun_namespace_id": "ash_tcu_k6zx_rehearsal_namespace_v1",
    "dryrun_namespace_created": true,
    "dryrun_namespace_isolated": true,
    "dryrun_namespace_persistent": false,
    "dryrun_namespace_user_visible": false,
    "dryrun_namespace_production_visible": false
  },
  "shadow_route_snapshot": {
    "pass": true,
    "shadow_route_snapshot_created": true,
    "snapshot_scope": "rehearsal_namespace_only",
    "snapshot_target_route": "current_default_route",
    "snapshot_candidate_route": "ash_tcu_k6p_row_major_emit_candidate_v1",
    "snapshot_hash_present": true,
    "snapshot_used_for_restore": true
  },
  "non_committing_runtime_splice_rehearsal": {
    "pass": true,
    "non_committing_runtime_splice_rehearsal_started": true,
    "non_committing_runtime_splice_rehearsal_completed": true,
    "runtime_splice_rehearsal_scope": "rehearsal_namespace_only",
    "runtime_splice_opened": false,
    "production_runtime_splice_opened": false,
    "persistent_runtime_splice_opened": false
  },
  "shadow_route_swap_rehearsal": {
    "pass": true,
    "shadow_route_swap_rehearsal_started": true,
    "shadow_route_swap_rehearsal_completed": true,
    "shadow_route_before": "current_default_route",
    "shadow_route_during": "ash_tcu_k6p_row_major_emit_candidate_v1",
    "shadow_route_after": "current_default_route"
  },
  "rollback_rehearsal": {
    "pass": true,
    "rollback_rehearsal_started": true,
    "rollback_rehearsal_completed": true,
    "rollback_rehearsal_scope": "rehearsal_namespace_only",
    "rollback_target_route": "current_default_route",
    "rollback_restored_route": "current_default_route",
    "rollback_executed_against_production": false
  },
  "post_rollback_restore_check": {
    "pass": true,
    "post_rollback_restore_check_passed": true,
    "shadow_route_restored": true,
    "default_route_registry_unchanged": true,
    "production_route_registry_unchanged": true,
    "user_visible_route_unchanged": true
  },
  "operator_gate_still_pending_guard": {
    "pass": true,
    "operator_gate_required": true,
    "operator_gate_state": "pending",
    "operator_approval_granted": false,
    "operator_approval_source": "none",
    "operator_approval_signature_present": false
  },
  "no_persistent_route_mutation_guard": {
    "pass": true,
    "default_route_registry_mutated": false,
    "production_route_registry_mutated": false,
    "user_visible_route_mutated": false,
    "base_train_route_registry_mutated": false
  },
  "verdict": {
    "pass": true,
    "verdict": "rollback_rehearsal_and_apply_dryrun_passed_no_default_adoption",
    "recommended_next_patch": "ASH-TCU-K6ZY_OPERATOR_APPROVAL_TOKEN_AND_GATED_APPLY_CANDIDATE_NO_DEFAULT_ADOPTION"
  }
}
```

## PASS Markers

```txt
PASS_ASH_TCU_K6ZX_PRIOR_K6ZW_APPLY_QUEUE_RECEIPT
PASS_ASH_TCU_K6ZX_DRYRUN_REHEARSAL_NAMESPACE
PASS_ASH_TCU_K6ZX_SHADOW_ROUTE_SNAPSHOT
PASS_ASH_TCU_K6ZX_NON_COMMITTING_RUNTIME_SPLICE_REHEARSAL
PASS_ASH_TCU_K6ZX_SHADOW_ROUTE_SWAP_REHEARSAL
PASS_ASH_TCU_K6ZX_ROLLBACK_REHEARSAL
PASS_ASH_TCU_K6ZX_POST_ROLLBACK_RESTORE_CHECK
PASS_ASH_TCU_K6ZX_OPERATOR_GATE_STILL_PENDING
PASS_ASH_TCU_K6ZX_NO_DEFAULT_ADOPTION
PASS_ASH_TCU_K6ZX_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K6ZX_NO_USER_VISIBLE_ADOPTION
PASS_ASH_TCU_K6ZX_NO_PERSISTENT_ROUTE_MUTATION
PASS_ASH_TCU_K6ZX_ROLLBACK_REHEARSAL_AND_APPLY_DRYRUN_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K6ZX_MISSING_K6ZW_PRIOR_VERDICT
FAIL_ASH_TCU_K6ZX_K6ZW_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K6ZX_K6ZW_APPLY_QUEUE_NOT_READY
FAIL_ASH_TCU_K6ZX_K6ZW_OPERATOR_GATE_NOT_PENDING
FAIL_ASH_TCU_K6ZX_K6ZW_ROLLBACK_PLAN_NOT_BOUND
FAIL_ASH_TCU_K6ZX_DRYRUN_NAMESPACE_NOT_CREATED
FAIL_ASH_TCU_K6ZX_DRYRUN_NAMESPACE_NOT_ISOLATED
FAIL_ASH_TCU_K6ZX_SHADOW_ROUTE_SNAPSHOT_MISSING
FAIL_ASH_TCU_K6ZX_NON_COMMITTING_SPLICE_REHEARSAL_NOT_RUN
FAIL_ASH_TCU_K6ZX_SHADOW_ROUTE_SWAP_REHEARSAL_NOT_RUN
FAIL_ASH_TCU_K6ZX_ROLLBACK_REHEARSAL_NOT_RUN
FAIL_ASH_TCU_K6ZX_POST_ROLLBACK_RESTORE_FAILED
FAIL_ASH_TCU_K6ZX_OPERATOR_APPROVAL_GRANTED
FAIL_ASH_TCU_K6ZX_APPLY_EXECUTION_STARTED
FAIL_ASH_TCU_K6ZX_APPLY_EXECUTION_COMPLETED
FAIL_ASH_TCU_K6ZX_RUNTIME_SPLICE_OPENED
FAIL_ASH_TCU_K6ZX_DEFAULT_ROUTE_MUTATED
FAIL_ASH_TCU_K6ZX_PRODUCTION_ROUTE_MUTATED
FAIL_ASH_TCU_K6ZX_USER_VISIBLE_ROUTE_MUTATED
FAIL_ASH_TCU_K6ZX_DEFAULT_ADOPTION_EXECUTED
FAIL_ASH_TCU_K6ZX_PRODUCTION_REPLACEMENT_EXECUTED
FAIL_ASH_TCU_K6ZX_USER_VISIBLE_ADOPTION_OPENED
FAIL_ASH_TCU_K6ZX_PERFORMANCE_CLAIM_ALLOWED
```

## Static Checks

```txt
required_prior_patch = ASH-TCU-K6ZW
required_prior_pass = true
k6zw_apply_queue_ready = true
k6zw_apply_queue_state = pending_operator_review
k6zw_operator_gate_required = true
k6zw_operator_approval_granted = false
k6zw_rollback_plan_bound = true
dryrun_namespace_created = true
dryrun_namespace_isolated = true
shadow_route_snapshot_created = true
non_committing_runtime_splice_rehearsal_completed = true
shadow_route_swap_rehearsal_completed = true
rollback_rehearsal_completed = true
post_rollback_restore_check_passed = true
operator_approval_granted = false
apply_execution_started = false
apply_execution_completed = false
runtime_splice_opened = false
default_route_registry_mutated = false
production_route_registry_mutated = false
user_visible_route_mutated = false
```

## Acceptance Criteria

```txt
1. K6ZW prior verdict exists.
2. K6ZW prior verdict status matches required PASS marker.
3. K6ZW apply queue is ready.
4. K6ZW apply queue state is pending_operator_review.
5. K6ZW operator gate is pending.
6. K6ZW rollback plan is bound.
7. K6ZX creates isolated dryrun namespace.
8. K6ZX snapshots shadow route.
9. K6ZX completes non-committing runtime splice rehearsal.
10. K6ZX completes shadow route swap rehearsal.
11. K6ZX completes rollback rehearsal.
12. K6ZX verifies post-rollback route restoration.
13. K6ZX keeps operator approval false.
14. K6ZX does not start real apply execution.
15. K6ZX does not complete real apply execution.
16. K6ZX does not open persistent runtime splice.
17. K6ZX does not mutate default route registry.
18. K6ZX does not mutate production route registry.
19. K6ZX does not mutate user-visible route.
20. K6ZX does not allow performance claim.
21. K6ZX recommends K6ZY as the next patch.
```

## Non-Mutation Seal

K6ZX must not write, mutate, or finalize:

```txt
model weights
optimizer state
safetensors checkpoint
runtime decode output
assistant message output
default route registry
production route registry
user-visible route registry
base_train route registry
persistent runtime splice state
```

K6ZX may write:

```txt
dryrun rehearsal receipt
shadow route snapshot receipt
non-committing splice rehearsal receipt
rollback rehearsal receipt
post-rollback restore check receipt
```

## Recommended Next Patch

```txt
ASH-TCU-K6ZY
Operator Approval Token And Gated Apply Candidate /
Pending Queue To Explicit Approval Receipt
No Default Adoption No Production Replacement Seal
```

## Final Seal

```txt
ASH-TCU-K6ZX does not make TensorCube production-ready.

ASH-TCU-K6ZX only converts K6ZW from:
apply_queue_entry_created_pending_operator_review_no_default_adoption

into:
rollback_rehearsal_and_apply_dryrun_passed_no_default_adoption

without granting operator approval, executing real apply, opening persistent runtime splice, changing default route, replacing production route, user-visible adoption, base_train, training, optimizer, or weight mutation.
```
