# ASH-TCU-K7E SPEC

## Title

Operator Review Token For Direct Default Adoption / Single-Use Direct Adoption Approval / No Shadow Rehearsal / No Production Replacement Seal

## Patch ID

```txt
ASH-TCU-K7E
```

## Status Target

```txt
PASS_ASH_TCU_K7E_OPERATOR_REVIEW_TOKEN_FOR_DIRECT_DEFAULT_ADOPTION_NO_SHADOW_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K7D
```

## Required Prior Status

```txt
PASS_ASH_TCU_K7D_INTERNAL_CANARY_PROMOTION_READINESS_PACKET_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
internal_canary_promotion_readiness_packet_created_no_default_adoption
```

## Superseded Previous Recommendation

K7D originally recommended a shadow default rehearsal patch. This is superseded by operator instruction:

```txt
shadow rehearsal excluded
direct default adoption gate selected
```

K7E must not create a shadow-default rehearsal route, namespace, probe, output quarantine, or any `shadow_default_*` runtime receipt.

## Purpose

`ASH-TCU-K7E` uses the K7D promotion readiness packet as the required parent state.

K7D proved that the candidate is ready for operator review while also proving that operator approval was not granted, no approval token was created, and no promotion execution started.

K7E is the first patch allowed to create an explicit single-use operator approval token for direct default adoption.

K7E does not execute default adoption.

K7E does not replace production.

K7E does not expose user-visible output.

K7E does not mutate model weights.

K7E does not run training, loss/backward, optimizer step, safetensors mutation, or checkpoint finalization.

K7E only converts the review packet state into an armed approval-token state for the next patch.

## Current K7D Baseline

K7D established:

```txt
candidate_ready_for_operator_review = true
candidate_production_ready = false
candidate_ready_for_default_adoption = false
operator_review_packet_created = true
operator_review_packet_requires_explicit_operator_approval = true
operator_review_packet_approval_granted = false
operator_review_packet_approval_token_created = false
operator_review_packet_single_use_token_required_next = true
promotion_execution_started = false
promotion_execution_completed = false
default_adoption_executed = false
production_replacement_executed = false
user_visible_adoption_executed = false
default_route_registry_mutated = false
production_route_registry_mutated = false
user_visible_route_mutated = false
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
performance_claim_allowed = false
```

K7E must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7e_direct_default_adoption_token_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7e_prior_k7d_readiness_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_operator_identity_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_direct_default_adoption_scope_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_direct_default_adoption_token_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_single_use_token_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_no_shadow_rehearsal_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_default_adoption_non_execution_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_no_user_visible_execution_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_no_performance_claim_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_static_checks_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_verdict_latest.json
artifacts/ASH_TCU_K7E_LOCAL_MANIFEST.json
```

## State Ownership

K7E owns prior K7D readiness receipt validation, operator identity packet, direct default adoption scope, direct default adoption token, single-use token guard, no-shadow rehearsal guard, default adoption non-execution guard, and no-production/no-user-visible/no-weight/no-performance guards.

K7E does not own default route adoption execution, production route replacement, user-visible adoption execution, assistant output mutation, runtime decode output mutation, base_train route binding, weight atlas construction, GPU streaming promotion, training, loss/backward, optimizer, weight commit, safetensors mutation, checkpoint finalization, or shadow default rehearsal.

## Source Inputs

K7E must read and validate the latest K7D receipts:

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7d_prior_k7c_rollback_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7d_evidence_chain_index_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7d_candidate_readiness_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7d_readiness_gate_eval_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7d_operator_review_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7d_candidate_review_state_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7d_promotion_non_execution_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7d_no_default_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7d_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7d_no_user_visible_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7d_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7d_no_performance_claim_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7d_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7d_static_checks_latest.json
artifacts/ASH_TCU_K7D_LOCAL_MANIFEST.json
```

K7E may read K6ZZ, K7A, K7B, and K7C receipts as historical evidence only. K7E must not recompute prior canary, stability, rollback, or readiness evidence.

## Candidate Route Lineage

K7E must preserve:

```txt
candidate_route_namespace_id = ash_tcu_k6zz_candidate_route_namespace_v1
internal_canary_namespace_id = ash_tcu_k7a_internal_canary_namespace_v1
candidate_readiness_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
candidate_readiness_route = ash_tcu_k6p_row_major_emit_candidate_v1
candidate_ready_for_operator_review = true
candidate_production_ready = false
```

K7E must not mutate candidate route, dtype, layout, tile mode, or evidence status.

## Operator Identity Packet

K7E must create an explicit operator identity packet:

```txt
operator_identity_packet_created = true
operator_identity_scope = direct_default_adoption_review
operator_identity_verified = true
operator_identity_signature_present = true
operator_identity_replay_protected = true
operator_identity_user_visible = false
```

The operator identity packet is required to create the direct adoption approval token. K7E must fail if the operator identity packet is missing or unverified.

## Direct Default Adoption Scope

K7E must create a direct adoption scope receipt:

```txt
direct_default_adoption_scope_created = true
direct_default_adoption_scope = direct_default_adoption_only
direct_default_adoption_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
direct_default_adoption_route = ash_tcu_k6p_row_major_emit_candidate_v1
direct_default_adoption_shadow_rehearsal_allowed = false
direct_default_adoption_production_replacement_allowed = false
direct_default_adoption_user_visible_execution_allowed = false
direct_default_adoption_weight_mutation_allowed = false
shadow_default_rehearsal_allowed = false
shadow_default_route_created = false
shadow_default_namespace_created = false
shadow_default_probe_executed = false
```

## Direct Default Adoption Approval Token

K7E must create a single-use approval token:

```txt
direct_default_adoption_token_created = true
direct_default_adoption_token_granted = true
direct_default_adoption_token_source = explicit_operator_review
direct_default_adoption_token_scope = direct_default_adoption_only
direct_default_adoption_token_single_use = true
direct_default_adoption_token_consumed = false
direct_default_adoption_token_reuse_allowed = false
direct_default_adoption_token_replay_protected = true
direct_default_adoption_token_signature_present = true
```

This token permits only the next patch to attempt direct default adoption execution. This token does not execute default adoption, replace production, expose user-visible output, or mutate weights.

## Guards

### Single-Use Token Guard

```txt
single_use_token_guard_created = true
token_single_use = true
token_consumed_before = false
token_consumed_after = false
token_reuse_allowed = false
token_replay_detected = false
token_scope = direct_default_adoption_only
```

### No Shadow Rehearsal Guard

```txt
no_shadow_rehearsal_guard_created = true
shadow_rehearsal_allowed = false
shadow_rehearsal_started = false
shadow_rehearsal_completed = false
shadow_default_route_created = false
shadow_default_namespace_created = false
shadow_default_probe_executed = false
shadow_default_output_quarantine_created = false
shadow_default_receipt_written = false
```

### Default Adoption Non-Execution Guard

```txt
default_adoption_non_execution_guard_created = true
default_adoption_token_created = true
default_adoption_execution_allowed_next = true
default_adoption_execution_started = false
default_adoption_execution_completed = false
default_adoption_executed = false
candidate_route_promoted_to_default = false
default_route_registry_mutated = false
global_default_route_changed = false
```

### No Production Replacement Guard

```txt
production_replacement_allowed = false
production_replacement_executed = false
candidate_route_promoted_to_production = false
production_route_registry_mutated = false
production_route_state_changed = false
```

### No User-Visible Execution Guard

```txt
user_visible_execution_allowed = false
user_visible_adoption_executed = false
candidate_route_promoted_to_user_visible = false
assistant_message_output_changed = false
runtime_decode_output_changed = false
user_visible_route_mutated = false
```

### No Weight Mutation Guard

```txt
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
weight_commit_executed = false
checkpoint_finalized = false
```

### No Performance Claim Guard

```txt
performance_claim_allowed = false
benchmark_claim_promoted = false
direct_default_token_promoted_to_performance_claim = false
operator_token_promoted_to_performance_claim = false
```

K7E may say a direct default adoption token is created. K7E must not say the candidate is production-ready or that default adoption has executed.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k7e_prior_k7d_readiness_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7e_operator_identity_packet.rs
crates/burn_webgpu_backend/src/tensorcube_k7e_direct_default_adoption_scope.rs
crates/burn_webgpu_backend/src/tensorcube_k7e_direct_default_adoption_token.rs
crates/burn_webgpu_backend/src/tensorcube_k7e_single_use_token_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7e_no_shadow_rehearsal_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7e_default_adoption_non_execution_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7e_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7e_no_user_visible_execution_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7e_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7e_no_performance_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7e_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7e_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7e_direct_default_adoption_token_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7e_direct_default_adoption_token_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7e_direct_default_adoption_token_audit -- --repo-root <repo> --require-k7d-pass --require-operator-review-ready --create-operator-identity-packet --create-direct-default-adoption-scope --create-direct-default-adoption-token --enforce-single-use-token --exclude-shadow-rehearsal --enforce-default-adoption-non-execution --no-production-replacement --no-user-visible-execution --no-weight-mutation --no-performance-claim
```

## PASS Markers

```txt
PASS_ASH_TCU_K7E_PRIOR_K7D_READINESS_RECEIPT
PASS_ASH_TCU_K7E_OPERATOR_IDENTITY_PACKET
PASS_ASH_TCU_K7E_DIRECT_DEFAULT_ADOPTION_SCOPE
PASS_ASH_TCU_K7E_DIRECT_DEFAULT_ADOPTION_TOKEN
PASS_ASH_TCU_K7E_SINGLE_USE_TOKEN_GUARD
PASS_ASH_TCU_K7E_NO_SHADOW_REHEARSAL
PASS_ASH_TCU_K7E_DEFAULT_ADOPTION_NON_EXECUTION
PASS_ASH_TCU_K7E_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K7E_NO_USER_VISIBLE_EXECUTION
PASS_ASH_TCU_K7E_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7E_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7E_OPERATOR_REVIEW_TOKEN_FOR_DIRECT_DEFAULT_ADOPTION_NO_SHADOW_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K7E_MISSING_K7D_PRIOR_VERDICT
FAIL_ASH_TCU_K7E_K7D_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K7E_CANDIDATE_NOT_READY_FOR_OPERATOR_REVIEW
FAIL_ASH_TCU_K7E_OPERATOR_REVIEW_PACKET_MISSING
FAIL_ASH_TCU_K7E_OPERATOR_IDENTITY_PACKET_MISSING
FAIL_ASH_TCU_K7E_OPERATOR_IDENTITY_NOT_VERIFIED
FAIL_ASH_TCU_K7E_DIRECT_DEFAULT_ADOPTION_SCOPE_MISSING
FAIL_ASH_TCU_K7E_DIRECT_DEFAULT_ADOPTION_TOKEN_NOT_CREATED
FAIL_ASH_TCU_K7E_DIRECT_DEFAULT_ADOPTION_TOKEN_NOT_GRANTED
FAIL_ASH_TCU_K7E_TOKEN_NOT_SINGLE_USE
FAIL_ASH_TCU_K7E_TOKEN_ALREADY_CONSUMED
FAIL_ASH_TCU_K7E_TOKEN_SCOPE_TOO_BROAD
FAIL_ASH_TCU_K7E_SHADOW_REHEARSAL_ALLOWED
FAIL_ASH_TCU_K7E_SHADOW_REHEARSAL_STARTED
FAIL_ASH_TCU_K7E_SHADOW_DEFAULT_ROUTE_CREATED
FAIL_ASH_TCU_K7E_SHADOW_DEFAULT_NAMESPACE_CREATED
FAIL_ASH_TCU_K7E_DEFAULT_ADOPTION_EXECUTION_STARTED
FAIL_ASH_TCU_K7E_DEFAULT_ADOPTION_EXECUTED
FAIL_ASH_TCU_K7E_DEFAULT_ROUTE_MUTATED
FAIL_ASH_TCU_K7E_PRODUCTION_REPLACEMENT_EXECUTED
FAIL_ASH_TCU_K7E_PRODUCTION_ROUTE_MUTATED
FAIL_ASH_TCU_K7E_USER_VISIBLE_EXECUTION_OPENED
FAIL_ASH_TCU_K7E_USER_VISIBLE_ROUTE_MUTATED
FAIL_ASH_TCU_K7E_WEIGHT_MUTATION_DETECTED
FAIL_ASH_TCU_K7E_PERFORMANCE_CLAIM_ALLOWED
```

## Recommended Next Patch

```txt
ASH-TCU-K7F
Direct Default Adoption Execution /
Consume Single-Use Direct Adoption Token /
Candidate Route Becomes Default /
No Production Replacement No Weight Mutation Seal
```

## Final Seal

```txt
ASH-TCU-K7E does not execute default adoption.

ASH-TCU-K7E only converts K7D from:
internal_canary_promotion_readiness_packet_created_no_default_adoption

into:
direct_default_adoption_operator_token_created_no_shadow_no_execution

without running shadow rehearsal, changing default route, replacing production route, exposing user-visible output, binding base_train, training, optimizer, or weight mutation.
```
