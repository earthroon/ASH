# ASH-TCU-K6ZT SPEC

## Title

Runtime Measurement Source Rebind / K6ZS Prior Receipt Evidence To Runtime Provenance Closure / No Static Metric Promotion No Apply Queue No Production Replacement Seal

## Patch ID

```txt
ASH-TCU-K6ZT
```

## Status Target

```txt
PASS_ASH_TCU_K6ZT_RUNTIME_MEASUREMENT_SOURCE_REBIND_NO_STATIC_METRIC_PROMOTION_NO_APPLY_QUEUE_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K6ZS
```

## Required Prior Status

```txt
PASS_ASH_TCU_K6ZS_LIMITED_PRODUCTION_SHADOW_PROMOTION_REVIEW_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Purpose

`ASH-TCU-K6ZT` closes the unresolved runtime measurement provenance gap detected by `ASH-TCU-K6ZS`.

`ASH-TCU-K6ZS` passed the limited production-shadow promotion review, but it intentionally did not mark the candidate as apply-ready because several evidence packets were classified as `prior_receipt_replayed` rather than freshly owned runtime-measured evidence.

This patch rebinds K6ZS/K6ZR-derived evidence into an explicit runtime provenance closure packet without promoting static, replayed, contract-generated, or unknown evidence into runtime-measured status.

## Current K6ZS Problem Statement

K6ZS produced a valid promotion review, but the following remained true:

```txt
apply_queue_ready = false
measurement_rebind_required = true
runtime_measurement_provenance_closed = false
static_metric_promoted_to_runtime_measured = false
unknown_source_promoted_to_apply_ready = false
production_replacement_executed = false
default_adoption_allowed = false
user_visible_adoption_allowed = false
```

K6ZT exists to close provenance ownership, not to open runtime adoption.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zt_runtime_measurement_source_rebind_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zt_prior_k6zs_verdict_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_evidence_source_rebind_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_runtime_provenance_closure_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_no_static_metric_promotion_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_no_apply_queue_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_static_checks_latest.json
artifacts/ASH_TCU_K6ZT_LOCAL_MANIFEST.json
```

## State Ownership

### K6ZT owns

```txt
runtime_measurement_source_rebind
runtime_provenance_closure
evidence_source_rebind_matrix
no_static_metric_promotion_guard
no_apply_queue_guard
no_production_replacement_guard
```

### K6ZT does not own

```txt
TensorCube candidate creation
K6P row-major candidate emit
K6ZQ limited production-shadow bind
K6ZR runtime monitor execution
K6ZS promotion review execution
native WGPU strict parity
apply queue entry
production replacement
default route adoption
user-visible route adoption
training execution
loss/backward execution
optimizer step
weight commit
safetensors mutation
checkpoint finalization
```

## Source Inputs

K6ZT must read, validate, and classify the latest K6ZS receipts:

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zs_promotion_review_config_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zs_prior_k6zr_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zs_k6zr_evidence_digest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zs_runtime_evidence_source_classification_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zs_shadow_health_review_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zs_divergence_evidence_review_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zs_timing_evidence_review_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zs_no_adoption_guard_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zs_production_replacement_block_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zs_next_patch_recommendation_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zs_promotion_review_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zs_bench_diagnosis_latest.json
```

## Evidence Source Classes

K6ZT must preserve the following evidence classes without silent conversion:

```txt
runtime_measured
prior_receipt_replayed
contract_generated
static_expected
unknown
```

## Rebind Policy

### Allowed

```txt
prior_receipt_replayed -> provenance_rebound_from_prior_receipt
contract_generated -> contract_guard_confirmed
runtime_measured -> runtime_measured_preserved
static_expected -> static_expected_preserved
unknown -> unknown_rejected_for_apply_ready
```

### Forbidden

```txt
prior_receipt_replayed -> runtime_measured
contract_generated -> runtime_measured
static_expected -> runtime_measured
unknown -> runtime_measured
unknown -> apply_ready
```

## Runtime Provenance Closure Semantics

K6ZT may set:

```txt
runtime_measurement_provenance_closed = true
```

only when all of the following are true:

```txt
k6zs_prior_verdict_valid = true
k6zs_required_status_matched = true
k6zs_measurement_rebind_required_was_true = true
evidence_source_rebind_matrix_generated = true
no_static_metric_promotion_guard_valid = true
unknown_source_apply_ready_rejection_valid = true
no_apply_queue_guard_valid = true
no_production_replacement_guard_valid = true
```

K6ZT must not set:

```txt
apply_queue_ready = true
```

This patch closes provenance only. Apply queue entry remains reserved for a later patch.

## Candidate Route

K6ZT must preserve the K6ZS candidate route metadata:

```txt
candidate_route = ash_tcu_k6p_row_major_emit_candidate_v1
candidate_dtype = f32
candidate_output_layout = row_major
candidate_shape = [256, 256, 32]
base_row_major_emit_patch = ASH-TCU-K6P
base_limited_production_shadow_bind_patch = ASH-TCU-K6ZQ
base_limited_production_shadow_runtime_monitor_patch = ASH-TCU-K6ZR
base_promotion_review_patch = ASH-TCU-K6ZS
```

K6ZT must not mutate candidate shape, dtype, route, or layout.

## Explicit Non-Scope

K6ZT does not enable:

```txt
native WGPU strict parity
new TensorCube dispatch path
new physical 16x16 WGSL kernel
runtime splice
production route replacement
default route adoption
user-visible output adoption
performance claim
apply queue entry
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

### No Static Metric Promotion Guard

K6ZT must verify:

```txt
static_metric_promoted_to_runtime_measured = false
prior_receipt_promoted_to_runtime_measured = false
contract_generated_promoted_to_runtime_measured = false
unknown_source_promoted_to_runtime_measured = false
```

### No Apply Queue Guard

K6ZT must verify:

```txt
apply_queue_ready = false
apply_queue_candidate_created = false
selected_next_patch_executed = false
operator_apply_gate_opened = false
```

### No Production Replacement Guard

K6ZT must verify:

```txt
production_replacement_allowed = false
production_replacement_executed = false
production_route_state_changed = false
global_default_route_changed = false
broad_rollout_state_changed = false
runtime_splice_opened = false
shadow_output_commit_executed = false
shadow_output_default_adoption_executed = false
shadow_output_user_visible_adoption_executed = false
```

### No Performance Claim Guard

K6ZT must verify:

```txt
performance_claim_allowed = false
benchmark_claim_promoted = false
timing_replay_claim_promoted = false
```

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k6zt_runtime_measurement_source_rebind.rs
crates/burn_webgpu_backend/src/tensorcube_k6zt_prior_k6zs_verdict_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k6zt_evidence_source_rebind_matrix.rs
crates/burn_webgpu_backend/src/tensorcube_k6zt_runtime_provenance_closure.rs
crates/burn_webgpu_backend/src/tensorcube_k6zt_no_static_metric_promotion.rs
crates/burn_webgpu_backend/src/tensorcube_k6zt_no_apply_queue_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zt_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zt_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k6zt_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k6zt_runtime_measurement_source_rebind_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k6zt_runtime_measurement_source_rebind_audit.rs
```

## Test Files

```txt
crates/burn_webgpu_backend/tests/ash_tcu_k6zt_prior_k6zs_verdict_receipt.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zt_evidence_source_rebind_matrix.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zt_runtime_provenance_closure.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zt_no_static_metric_promotion.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zt_no_apply_queue_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zt_no_production_replacement_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zt_verdict.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zt_rebind_disposition.rs
```

## CLI

### Binary

```txt
ash_tcu_k6zt_runtime_measurement_source_rebind_audit
```

### Command

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k6zt_runtime_measurement_source_rebind_audit -- --repo-root <repo> --require-k6zs-pass --rebind-prior-receipt-evidence --close-runtime-provenance --reject-static-metric-promotion --reject-unknown-source-apply-ready --no-apply-queue --no-production-replacement --no-default-adoption --no-user-visible-adoption
```

Optional handoff import command for replaying a pasted K6ZS report:

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k6zt_runtime_measurement_source_rebind_audit -- --repo-root <repo> --k6zs-report-json <k6zs-report-json-or-log> --require-k6zs-pass --rebind-prior-receipt-evidence --close-runtime-provenance --reject-static-metric-promotion --reject-unknown-source-apply-ready --no-apply-queue --no-production-replacement --no-default-adoption --no-user-visible-adoption
```

## Required Output JSON Shape

```json
{
  "patch_id": "ASH-TCU-K6ZT",
  "status": "PASS_ASH_TCU_K6ZT_RUNTIME_MEASUREMENT_SOURCE_REBIND_NO_STATIC_METRIC_PROMOTION_NO_APPLY_QUEUE_NO_PRODUCTION_REPLACEMENT_SEAL",
  "prior_k6zs_verdict_receipt": {
    "pass": true,
    "k6zs_required": true,
    "k6zs_valid": true,
    "k6zs_status": "PASS_ASH_TCU_K6ZS_LIMITED_PRODUCTION_SHADOW_PROMOTION_REVIEW_NO_PRODUCTION_REPLACEMENT_SEAL",
    "k6zs_measurement_rebind_required": true,
    "k6zs_apply_queue_ready": false
  },
  "evidence_source_rebind_matrix": {
    "pass": true,
    "prior_receipt_replayed_rebound": true,
    "contract_generated_preserved": true,
    "static_expected_preserved": true,
    "unknown_rejected_for_apply_ready": true,
    "runtime_measured_preserved": true,
    "prior_receipt_promoted_to_runtime_measured": false,
    "unknown_source_promoted_to_apply_ready": false
  },
  "runtime_provenance_closure": {
    "pass": true,
    "runtime_measurement_provenance_closed": true,
    "measurement_rebind_required": false
  },
  "no_apply_queue_guard": {
    "pass": true,
    "apply_queue_ready": false,
    "apply_queue_candidate_created": false,
    "operator_apply_gate_opened": false
  },
  "no_production_replacement_guard": {
    "pass": true,
    "production_replacement_executed": false,
    "global_default_route_changed": false,
    "runtime_splice_opened": false,
    "user_visible_adoption_allowed": false
  },
  "verdict": {
    "pass": true,
    "verdict": "runtime_measurement_source_rebind_pass_no_apply_queue",
    "recommended_next_patch": "ASH-TCU-K6ZU_RUNTIME_MEASURED_SHADOW_REPLAY_EVIDENCE_CLOSURE"
  }
}
```

## PASS Markers

The audit must print:

```txt
PASS_ASH_TCU_K6ZT_PRIOR_K6ZS_VERDICT_RECEIPT
PASS_ASH_TCU_K6ZT_EVIDENCE_SOURCE_REBIND_MATRIX
PASS_ASH_TCU_K6ZT_RUNTIME_PROVENANCE_CLOSURE
PASS_ASH_TCU_K6ZT_NO_STATIC_METRIC_PROMOTION
PASS_ASH_TCU_K6ZT_NO_APPLY_QUEUE
PASS_ASH_TCU_K6ZT_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K6ZT_RUNTIME_MEASUREMENT_SOURCE_REBIND_NO_STATIC_METRIC_PROMOTION_NO_APPLY_QUEUE_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

The audit must fail with explicit markers:

```txt
FAIL_ASH_TCU_K6ZT_MISSING_K6ZS_PRIOR_VERDICT
FAIL_ASH_TCU_K6ZT_K6ZS_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K6ZT_K6ZS_DID_NOT_REQUIRE_MEASUREMENT_REBIND
FAIL_ASH_TCU_K6ZT_PRIOR_RECEIPT_PROMOTED_TO_RUNTIME_MEASURED
FAIL_ASH_TCU_K6ZT_CONTRACT_GENERATED_PROMOTED_TO_RUNTIME_MEASURED
FAIL_ASH_TCU_K6ZT_STATIC_METRIC_PROMOTED_TO_RUNTIME_MEASURED
FAIL_ASH_TCU_K6ZT_UNKNOWN_SOURCE_PROMOTED_TO_APPLY_READY
FAIL_ASH_TCU_K6ZT_RUNTIME_PROVENANCE_NOT_CLOSED
FAIL_ASH_TCU_K6ZT_APPLY_QUEUE_OPENED
FAIL_ASH_TCU_K6ZT_PRODUCTION_REPLACEMENT_EXECUTED
FAIL_ASH_TCU_K6ZT_DEFAULT_ROUTE_CHANGED
FAIL_ASH_TCU_K6ZT_USER_VISIBLE_ADOPTION_OPENED
FAIL_ASH_TCU_K6ZT_PERFORMANCE_CLAIM_ALLOWED
```

## Static Checks

The static checks receipt must verify:

```txt
required_prior_patch = ASH-TCU-K6ZS
required_prior_pass = true
measurement_rebind_required_before = true
measurement_rebind_required_after = false
runtime_measurement_provenance_closed_after = true
apply_queue_ready = false
production_replacement_executed = false
global_default_route_changed = false
static_metric_promoted_to_runtime_measured = false
unknown_source_promoted_to_apply_ready = false
```

## Acceptance Criteria

K6ZT is accepted only if all of the following are true:

```txt
1. K6ZS prior verdict exists.
2. K6ZS prior verdict status matches required PASS marker.
3. K6ZS measurement_rebind_required was true.
4. K6ZT evidence source rebind matrix is generated.
5. K6ZT preserves source classes without silent promotion.
6. K6ZT closes runtime provenance.
7. K6ZT clears measurement_rebind_required.
8. K6ZT does not create apply queue candidate.
9. K6ZT does not open production replacement.
10. K6ZT does not change default route.
11. K6ZT does not allow user-visible adoption.
12. K6ZT does not allow performance claim.
13. K6ZT recommends K6ZU as the next patch.
```

## Non-Mutation Seal

K6ZT must not write, mutate, or finalize:

```txt
model weights
optimizer state
safetensors checkpoint
runtime decode output
assistant message output
default route registry
production route registry
apply queue state
rollback state
```

## Recommended Next Patch

```txt
ASH-TCU-K6ZU
Runtime-Measured Shadow Replay Evidence Closure /
K6ZT Provenance Closure To Fresh Runtime Replay Packet
No Apply Queue No Production Replacement Seal
```

## Final Seal

```txt
ASH-TCU-K6ZT does not make TensorCube production-ready.

ASH-TCU-K6ZT only converts K6ZS from:
promotion_review_pass_measurement_rebind_required

into:
runtime_measurement_source_rebind_pass_no_apply_queue

without opening apply queue, production replacement, default adoption, user-visible adoption, training, optimizer, or weight mutation.
```
