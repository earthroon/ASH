# ASH-TCU-K6ZU SPEC

## Title

Runtime-Measured Shadow Replay Evidence Closure / K6ZT Provenance Closure To Fresh Runtime Replay Packet / No Apply Queue No Production Replacement Seal

## Patch ID

```txt
ASH-TCU-K6ZU
```

## Status Target

```txt
PASS_ASH_TCU_K6ZU_RUNTIME_MEASURED_SHADOW_REPLAY_EVIDENCE_CLOSURE_NO_APPLY_QUEUE_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K6ZT
```

## Required Prior Status

```txt
PASS_ASH_TCU_K6ZT_RUNTIME_MEASUREMENT_SOURCE_REBIND_NO_STATIC_METRIC_PROMOTION_NO_APPLY_QUEUE_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
runtime_measurement_source_rebind_pass_no_apply_queue
```

## Purpose

`ASH-TCU-K6ZU` uses the K6ZT provenance closure as the required parent state and produces a fresh runtime-measured shadow replay evidence packet.

K6ZT closed the measurement provenance gap by rebinding K6ZS prior receipt evidence without promoting replayed, static, contract-generated, or unknown evidence into runtime-measured status.

K6ZU is the next step. It must execute a fresh runtime replay over the existing limited production-shadow candidate scope and produce newly measured shadow health, timing, divergence, parity, and non-commit evidence.

K6ZU still does not open apply queue, production replacement, default adoption, user-visible adoption, base_train, loss/backward, optimizer, weight commit, or checkpoint mutation.

## Current K6ZT Baseline

K6ZT established:

```txt
runtime_measurement_provenance_closed = true
measurement_rebind_required = false
apply_queue_ready = false
production_replacement_executed = false
global_default_route_changed = false
static_metric_promoted_to_runtime_measured = false
unknown_source_promoted_to_apply_ready = false
recommended_next_patch = ASH-TCU-K6ZU_RUNTIME_MEASURED_SHADOW_REPLAY_EVIDENCE_CLOSURE
```

K6ZU must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zu_runtime_measured_shadow_replay_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zu_prior_k6zt_provenance_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zu_shadow_replay_config_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zu_shadow_health_runtime_measure_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zu_shadow_timing_runtime_measure_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zu_shadow_divergence_runtime_measure_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zu_shadow_parity_runtime_measure_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zu_shadow_non_commit_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zu_no_apply_queue_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zu_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zu_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zu_static_checks_latest.json
artifacts/ASH_TCU_K6ZU_LOCAL_MANIFEST.json
```

## State Ownership

### K6ZU owns

```txt
fresh_runtime_shadow_replay
runtime_measured_shadow_health_packet
runtime_measured_shadow_timing_packet
runtime_measured_shadow_divergence_packet
runtime_measured_shadow_parity_packet
shadow_non_commit_guard
no_apply_queue_guard
no_production_replacement_guard
```

### K6ZU does not own

```txt
TensorCube candidate creation
K6P row-major candidate emit
K6ZQ limited production-shadow bind
K6ZR original runtime monitor
K6ZS promotion review
K6ZT provenance rebind
native WGPU strict parity
apply queue entry
production replacement
default route adoption
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

K6ZU must read and validate the latest K6ZT receipts:

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zt_prior_k6zs_verdict_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_evidence_source_rebind_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_runtime_measurement_source_rebind_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_runtime_provenance_closure_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_no_static_metric_promotion_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_no_apply_queue_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zt_static_checks_latest.json
artifacts/ASH_TCU_K6ZT_LOCAL_MANIFEST.json
```

K6ZU may also read K6ZR/K6ZS metadata only as configuration source, not as runtime-measured evidence:

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zs_promotion_review_config_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zs_prior_k6zr_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zs_k6zr_evidence_digest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zs_runtime_evidence_source_classification_latest.json
```

## Replay Scope

K6ZU must preserve the K6ZS/K6ZT candidate metadata:

```txt
candidate_route = ash_tcu_k6p_row_major_emit_candidate_v1
candidate_dtype = f32
candidate_output_layout = row_major
candidate_shape = [256, 256, 32]
base_row_major_emit_patch = ASH-TCU-K6P
base_limited_production_shadow_bind_patch = ASH-TCU-K6ZQ
base_limited_production_shadow_runtime_monitor_patch = ASH-TCU-K6ZR
base_promotion_review_patch = ASH-TCU-K6ZS
base_provenance_closure_patch = ASH-TCU-K6ZT
```

K6ZU must not mutate candidate shape, dtype, route, or layout.

## Shadow Replay Configuration

K6ZU must run a fresh runtime shadow replay using deterministic scope:

```txt
shadow_scope = limited_production_shadow_canary
shadow_mode = runtime_measured_replay
shadow_health_window_count = 8
shadow_probe_seed_count = 16
shadow_probe_total = 128
candidate_output_commit_allowed = false
production_output_commit_allowed = false
readback_allowed = diagnostic_only
```

If the implementation cannot run the full 128-probe replay, it must fail or explicitly report `NOT_RUN`, not silently shrink the replay scope.

## Evidence Source Classification

K6ZU must produce fresh evidence classified as:

```txt
runtime_measured
```

for the following packets:

```txt
shadow_health_runtime_measure
shadow_timing_runtime_measure
shadow_divergence_runtime_measure
shadow_parity_runtime_measure
shadow_non_commit_guard
```

K6ZU must not reuse `prior_receipt_replayed` packets as runtime-measured output.

## Runtime Measurement Rules

### Allowed

```txt
fresh runtime shadow replay
deterministic probe replay
diagnostic readback
runtime timing measurement
runtime divergence measurement
runtime parity measurement
runtime health window measurement
non-commit guard verification
```

### Forbidden

```txt
prior receipt replay promoted to runtime measurement
contract-generated evidence promoted to runtime measurement
static expected metric promoted to runtime measurement
unknown source promoted to apply-ready
apply queue entry
production replacement
default route adoption
user-visible output adoption
performance claim
```

## Runtime-Measured Shadow Replay Semantics

K6ZU may set:

```txt
fresh_runtime_replay_executed = true
runtime_shadow_replay_evidence_closed = true
runtime_measured_shadow_health_valid = true
runtime_measured_shadow_timing_valid = true
runtime_measured_shadow_divergence_valid = true
runtime_measured_shadow_parity_valid = true
```

only when all of the following are true:

```txt
k6zt_prior_verdict_valid = true
k6zt_runtime_measurement_provenance_closed = true
k6zt_measurement_rebind_required = false
k6zt_apply_queue_ready = false
shadow_replay_config_valid = true
fresh_runtime_shadow_replay_executed = true
shadow_probe_total = 128
shadow_health_window_count = 8
shadow_probe_seed_count = 16
diagnostic_readback_only = true
shadow_output_commit_executed = false
production_replacement_executed = false
```

K6ZU must not set:

```txt
apply_queue_ready = true
```

Apply queue entry remains reserved for `ASH-TCU-K6ZV` or later, after native WGPU strict parity and replay evidence closure are both valid.

## Explicit Non-Scope

K6ZU does not enable:

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

### Prior K6ZT Provenance Guard

K6ZU must verify:

```txt
required_prior_patch = ASH-TCU-K6ZT
required_prior_pass = true
k6zt_runtime_measurement_provenance_closed = true
k6zt_measurement_rebind_required = false
k6zt_apply_queue_ready = false
k6zt_static_metric_promoted_to_runtime_measured = false
k6zt_unknown_source_promoted_to_apply_ready = false
```

### Fresh Runtime Replay Guard

K6ZU must verify:

```txt
fresh_runtime_shadow_replay_executed = true
runtime_replay_source_class = runtime_measured
prior_receipt_replay_used_as_measurement = false
contract_generated_used_as_measurement = false
static_expected_used_as_measurement = false
unknown_source_used_as_measurement = false
```

### Shadow Non-Commit Guard

K6ZU must verify:

```txt
shadow_output_commit_executed = false
shadow_output_default_adoption_executed = false
shadow_output_user_visible_adoption_executed = false
runtime_sequence_append_executed = false
kv_cache_mutation_executed = false
```

### No Apply Queue Guard

K6ZU must verify:

```txt
apply_queue_ready = false
apply_queue_candidate_created = false
selected_next_patch_executed = false
operator_apply_gate_opened = false
```

### No Production Replacement Guard

K6ZU must verify:

```txt
production_replacement_allowed = false
production_replacement_executed = false
production_route_state_changed = false
global_default_route_changed = false
broad_rollout_state_changed = false
runtime_splice_opened = false
```

### No Performance Claim Guard

K6ZU must verify:

```txt
performance_claim_allowed = false
benchmark_claim_promoted = false
timing_measurement_claim_promoted = false
```

K6ZU may report runtime measurements, but it must not claim production performance superiority.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k6zu_prior_k6zt_provenance_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k6zu_shadow_replay_config.rs
crates/burn_webgpu_backend/src/tensorcube_k6zu_runtime_measured_shadow_replay.rs
crates/burn_webgpu_backend/src/tensorcube_k6zu_shadow_health_runtime_measure.rs
crates/burn_webgpu_backend/src/tensorcube_k6zu_shadow_timing_runtime_measure.rs
crates/burn_webgpu_backend/src/tensorcube_k6zu_shadow_divergence_runtime_measure.rs
crates/burn_webgpu_backend/src/tensorcube_k6zu_shadow_parity_runtime_measure.rs
crates/burn_webgpu_backend/src/tensorcube_k6zu_shadow_non_commit_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zu_no_apply_queue_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zu_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zu_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k6zu_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k6zu_runtime_measured_shadow_replay_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k6zu_runtime_measured_shadow_replay_audit.rs
```

## Test Files

```txt
crates/burn_webgpu_backend/tests/ash_tcu_k6zu_prior_k6zt_provenance_receipt.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zu_shadow_replay_config.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zu_runtime_measured_shadow_replay.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zu_shadow_health_runtime_measure.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zu_shadow_timing_runtime_measure.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zu_shadow_divergence_runtime_measure.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zu_shadow_parity_runtime_measure.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zu_shadow_non_commit_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zu_no_apply_queue_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zu_no_production_replacement_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zu_verdict.rs
```

## Rust Module Export Requirements

### burn_webgpu_backend lib exports

`crates/burn_webgpu_backend/src/lib.rs` must expose:

```rust
pub mod tensorcube_k6zu_prior_k6zt_provenance_receipt;
pub mod tensorcube_k6zu_shadow_replay_config;
pub mod tensorcube_k6zu_runtime_measured_shadow_replay;
pub mod tensorcube_k6zu_shadow_health_runtime_measure;
pub mod tensorcube_k6zu_shadow_timing_runtime_measure;
pub mod tensorcube_k6zu_shadow_divergence_runtime_measure;
pub mod tensorcube_k6zu_shadow_parity_runtime_measure;
pub mod tensorcube_k6zu_shadow_non_commit_guard;
pub mod tensorcube_k6zu_no_apply_queue_guard;
pub mod tensorcube_k6zu_no_production_replacement_guard;
pub mod tensorcube_k6zu_verdict;
pub mod tensorcube_k6zu_contract_audit;
```

### orchestrator_local lib exports

`crates/orchestrator_local/src/lib.rs` must expose:

```rust
pub mod ash_tcu_k6zu_runtime_measured_shadow_replay_report;
```

## CLI

### Binary

```txt
ash_tcu_k6zu_runtime_measured_shadow_replay_audit
```

### Command

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k6zu_runtime_measured_shadow_replay_audit -- --repo-root <repo> --require-k6zt-pass --require-runtime-provenance-closed --run-fresh-shadow-replay --shadow-health-windows 8 --shadow-probe-seeds 16 --require-probe-total 128 --diagnostic-readback-only --reject-prior-receipt-as-runtime-measured --reject-static-metric-promotion --reject-unknown-source-apply-ready --no-apply-queue --no-production-replacement --no-default-adoption --no-user-visible-adoption
```

### Optional report input

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k6zu_runtime_measured_shadow_replay_audit -- --repo-root <repo> --k6zt-report-json <k6zt-report-json-or-log> --require-k6zt-pass --require-runtime-provenance-closed --run-fresh-shadow-replay --shadow-health-windows 8 --shadow-probe-seeds 16 --require-probe-total 128 --diagnostic-readback-only --reject-prior-receipt-as-runtime-measured --reject-static-metric-promotion --reject-unknown-source-apply-ready --no-apply-queue --no-production-replacement --no-default-adoption --no-user-visible-adoption
```

## Required Output JSON Shape

```json
{
  "patch_id": "ASH-TCU-K6ZU",
  "status": "PASS_ASH_TCU_K6ZU_RUNTIME_MEASURED_SHADOW_REPLAY_EVIDENCE_CLOSURE_NO_APPLY_QUEUE_NO_PRODUCTION_REPLACEMENT_SEAL",
  "prior_k6zt_provenance_receipt": {
    "pass": true,
    "k6zt_required": true,
    "k6zt_valid": true,
    "k6zt_status": "PASS_ASH_TCU_K6ZT_RUNTIME_MEASUREMENT_SOURCE_REBIND_NO_STATIC_METRIC_PROMOTION_NO_APPLY_QUEUE_NO_PRODUCTION_REPLACEMENT_SEAL",
    "k6zt_runtime_measurement_provenance_closed": true,
    "k6zt_measurement_rebind_required": false,
    "k6zt_apply_queue_ready": false
  },
  "shadow_replay_config": {
    "pass": true,
    "shadow_scope": "limited_production_shadow_canary",
    "shadow_mode": "runtime_measured_replay",
    "shadow_health_window_count": 8,
    "shadow_probe_seed_count": 16,
    "shadow_probe_total": 128,
    "candidate_route": "ash_tcu_k6p_row_major_emit_candidate_v1",
    "candidate_dtype": "f32",
    "candidate_output_layout": "row_major",
    "candidate_shape": [256, 256, 32]
  },
  "runtime_measured_shadow_replay": {
    "pass": true,
    "fresh_runtime_shadow_replay_executed": true,
    "runtime_replay_source_class": "runtime_measured",
    "prior_receipt_replay_used_as_measurement": false,
    "contract_generated_used_as_measurement": false,
    "static_expected_used_as_measurement": false,
    "unknown_source_used_as_measurement": false
  },
  "shadow_non_commit_guard": {
    "pass": true,
    "shadow_output_commit_executed": false,
    "runtime_sequence_append_executed": false,
    "kv_cache_mutation_executed": false
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
    "verdict": "runtime_measured_shadow_replay_evidence_closed_no_apply_queue",
    "recommended_next_patch": "ASH-TCU-K6ZV_LOGICAL16_NATIVE_WGPU_STRICT_PARITY_NO_CPU_RUNTIME_SELECTION"
  }
}
```

## PASS Markers

The audit must print:

```txt
PASS_ASH_TCU_K6ZU_PRIOR_K6ZT_PROVENANCE_RECEIPT
PASS_ASH_TCU_K6ZU_SHADOW_REPLAY_CONFIG
PASS_ASH_TCU_K6ZU_RUNTIME_MEASURED_SHADOW_REPLAY
PASS_ASH_TCU_K6ZU_SHADOW_HEALTH_RUNTIME_MEASURE
PASS_ASH_TCU_K6ZU_SHADOW_TIMING_RUNTIME_MEASURE
PASS_ASH_TCU_K6ZU_SHADOW_DIVERGENCE_RUNTIME_MEASURE
PASS_ASH_TCU_K6ZU_SHADOW_PARITY_RUNTIME_MEASURE
PASS_ASH_TCU_K6ZU_SHADOW_NON_COMMIT_GUARD
PASS_ASH_TCU_K6ZU_NO_APPLY_QUEUE
PASS_ASH_TCU_K6ZU_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K6ZU_RUNTIME_MEASURED_SHADOW_REPLAY_EVIDENCE_CLOSURE_NO_APPLY_QUEUE_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

The audit must fail with explicit markers:

```txt
FAIL_ASH_TCU_K6ZU_MISSING_K6ZT_PRIOR_VERDICT
FAIL_ASH_TCU_K6ZU_K6ZT_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K6ZU_K6ZT_PROVENANCE_NOT_CLOSED
FAIL_ASH_TCU_K6ZU_K6ZT_MEASUREMENT_REBIND_STILL_REQUIRED
FAIL_ASH_TCU_K6ZU_SHADOW_REPLAY_CONFIG_INVALID
FAIL_ASH_TCU_K6ZU_FRESH_RUNTIME_REPLAY_NOT_EXECUTED
FAIL_ASH_TCU_K6ZU_PROBE_TOTAL_MISMATCH
FAIL_ASH_TCU_K6ZU_PRIOR_RECEIPT_USED_AS_RUNTIME_MEASUREMENT
FAIL_ASH_TCU_K6ZU_CONTRACT_GENERATED_USED_AS_RUNTIME_MEASUREMENT
FAIL_ASH_TCU_K6ZU_STATIC_EXPECTED_USED_AS_RUNTIME_MEASUREMENT
FAIL_ASH_TCU_K6ZU_UNKNOWN_SOURCE_USED_AS_RUNTIME_MEASUREMENT
FAIL_ASH_TCU_K6ZU_SHADOW_HEALTH_RUNTIME_MEASURE_INVALID
FAIL_ASH_TCU_K6ZU_SHADOW_TIMING_RUNTIME_MEASURE_INVALID
FAIL_ASH_TCU_K6ZU_SHADOW_DIVERGENCE_RUNTIME_MEASURE_INVALID
FAIL_ASH_TCU_K6ZU_SHADOW_PARITY_RUNTIME_MEASURE_INVALID
FAIL_ASH_TCU_K6ZU_SHADOW_OUTPUT_COMMITTED
FAIL_ASH_TCU_K6ZU_APPLY_QUEUE_OPENED
FAIL_ASH_TCU_K6ZU_PRODUCTION_REPLACEMENT_EXECUTED
FAIL_ASH_TCU_K6ZU_DEFAULT_ROUTE_CHANGED
FAIL_ASH_TCU_K6ZU_USER_VISIBLE_ADOPTION_OPENED
FAIL_ASH_TCU_K6ZU_PERFORMANCE_CLAIM_ALLOWED
```

## Static Checks

The static checks receipt must verify:

```txt
required_prior_patch = ASH-TCU-K6ZT
required_prior_pass = true
runtime_measurement_provenance_closed_before = true
measurement_rebind_required_before = false
fresh_runtime_shadow_replay_executed = true
runtime_shadow_replay_evidence_closed = true
shadow_probe_total = 128
apply_queue_ready = false
production_replacement_executed = false
global_default_route_changed = false
shadow_output_commit_executed = false
static_metric_promoted_to_runtime_measured = false
unknown_source_promoted_to_apply_ready = false
```

## Acceptance Criteria

K6ZU is accepted only if all of the following are true:

```txt
1. K6ZT prior verdict exists.
2. K6ZT prior verdict status matches required PASS marker.
3. K6ZT runtime provenance closure is true.
4. K6ZT measurement_rebind_required is false.
5. K6ZU shadow replay config is generated and valid.
6. K6ZU executes fresh runtime shadow replay.
7. K6ZU generates runtime-measured shadow health evidence.
8. K6ZU generates runtime-measured shadow timing evidence.
9. K6ZU generates runtime-measured shadow divergence evidence.
10. K6ZU generates runtime-measured shadow parity evidence.
11. K6ZU does not use prior receipt replay as runtime measurement.
12. K6ZU does not use contract-generated evidence as runtime measurement.
13. K6ZU does not use static expected evidence as runtime measurement.
14. K6ZU does not use unknown source evidence as runtime measurement.
15. K6ZU does not commit shadow output.
16. K6ZU does not create apply queue candidate.
17. K6ZU does not open production replacement.
18. K6ZU does not change default route.
19. K6ZU does not allow user-visible adoption.
20. K6ZU does not allow performance claim.
21. K6ZU recommends K6ZV as the next patch.
```

## Non-Mutation Seal

K6ZU must not write, mutate, or finalize:

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
base_train state
```

## Recommended Next Patch

```txt
ASH-TCU-K6ZV
Logical16 Native WGPU Strict Parity /
K6ZU Runtime-Measured Shadow Replay To Native Dispatch Evidence
No CPU Runtime Selection No Apply Queue No Production Replacement Seal
```

## Final Seal

```txt
ASH-TCU-K6ZU does not make TensorCube production-ready.

ASH-TCU-K6ZU only converts K6ZT from:
runtime_measurement_source_rebind_pass_no_apply_queue

into:
runtime_measured_shadow_replay_evidence_closed_no_apply_queue

without opening apply queue, production replacement, default adoption, user-visible adoption, base_train, training, optimizer, or weight mutation.
```
