# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3

## Device-Native Guard Decision Token /
## GPU-Gated Downstream Consumption /
## Asynchronous Compact Telemetry Drain /
## Zero Hot-Path Host Wait Seal

---

## 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R2
parent_runtime_schema=ash.attn.headwise.causal.01b.r12.r2.runtime_artifact.v1
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.runtime_artifact.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3
attention_kernel_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
finite_guard_numeric_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R1
persistent_ring_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R2
device_decision_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3
promotion_scope=incremental_decode_only
```

R12-R3 preserves the R10 attention kernels and the R12-R1 IEEE-754 finite classification. It moves the scoped guard decision from a per-candidate host readback into a GPU-owned decision token.

---

## 1. Parent HOLD binding

Required parent files:

```text
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r2_runtime_artifact.json
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r2_local_manifest.json
```

Required parent state:

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R2
build_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R2
pass=false
status=HOLD
production_pass=true
guard_pass=true
policy_pass=true
negative_control_pass=true
performance_pass=false
```

Allowed parent failure components:

```text
guarded_performance_true_round_non_regression
static_truth_checks
canonical_negative_truth:StaticTruthFailure
```

The parent must contain the performance failure. No production, finite classification, policy, or negative-control runtime failure is admissible.

---

## 2. Problem

R12-R2 removed per-candidate guard allocation and separate submission but retained:

```text
GPU finite guard
→ map_async compact result
→ blocking device poll
→ CPU guard decision
→ next GPU work
```

The remaining GPU-to-CPU-to-GPU synchronization caused long-sequence regression. R12-R3 changes the authority path to:

```text
GPU attention candidate
→ GPU finite classification
→ GPU decision-token finalization
→ indirect GPU-gated downstream staging
→ later non-hot-path telemetry drain
```

---

## 3. Authority SSOT

The scoped authority SSOT is:

```text
DeviceGuardDecisionToken
```

The host telemetry mirror is evidence only. It cannot grant authority to GPU work and is not consulted in the candidate hot path.

Required host counters:

```text
hot_path_map_async_count=0
hot_path_blocking_poll_count=0
hot_path_blocking_receive_count=0
hot_path_host_guard_decision_count=0
```

---

## 4. Implemented downstream boundary

R12-R3 implements:

```text
candidate attention output
→ finite guard
→ device decision token
→ dispatch_workgroups_indirect
→ guarded downstream staging tensor
→ existing Burn o_proj consumes staging tensor
```

Accepted token:

```text
indirect workgroup count > 0
candidate values copied into downstream staging
```

Rejected token:

```text
indirect workgroup count = 0
downstream staging was cleared before dispatch
candidate values are not visible to o_proj
attention contribution entering o_proj is zero
```

Truth boundary:

```text
direct_o_proj_indirect_dispatch_proven=false
direct_o_proj_zero_invocation_proven=false
candidate_value_visibility_on_reject=false
same_device_downstream_gate_proven=true
```

R12-R3 does not claim that the existing Burn matmul invocation itself becomes a zero-workgroup indirect dispatch. That requires a later native linear/o_proj patch.

---

## 5. Device token layout

The token contains:

```text
downstream indirect dispatch x/y/z
authority_granted
failure_bits
candidate nonce
slot index
slot generation
expected element count
visited element count
non-finite counters
completion marker
token state
```

Decision formula:

```text
authority_granted =
  completion marker exact
  && candidate nonce exact
  && slot index exact
  && slot generation exact
  && expected element count == visited element count
  && non_finite_count == 0
  && nan_count == 0
  && positive_infinity_count == 0
  && negative_infinity_count == 0
  && guard_error_bits == 0
```

The token is initialized fail-closed. Before decision finalization:

```text
authority_granted=0
indirect dispatch x/y/z=0
```

---

## 6. GPU ordering

One command encoder records:

```text
1. clear finite-guard result
2. clear decision token
3. clear downstream staging tensor
4. attention compute pass
5. finite-classification compute pass
6. decision-token finalization pass
7. downstream staging indirect-dispatch pass
8. token copy into telemetry ring
9. one queue submission
```

Required per candidate:

```text
command_encoder_count=1
queue_submit_count=1
attention_dispatch_count=1
guard_dispatch_count=1
decision_dispatch_count=1
downstream_indirect_dispatch_count=1
```

The compute-pass boundaries establish the storage write/read ordering.

---

## 7. Device fault latch

A rejected token updates a device-owned first-failure latch:

```text
faulted
first_failure_bits
first_candidate_nonce
failure_count
```

The first failure cannot be overwritten by a later candidate without explicit session reset. Once latched, later device decisions fail closed with `FAILURE_SESSION_LATCHED`; a later finite candidate cannot silently restore Atlas staging authority.

---

## 8. Telemetry ring

Canonical configuration:

```text
decision_token_ring_capacity=4
telemetry_ring_capacity=4096
```

Each candidate copies one compact token record into the telemetry ring. Tensor values are never written into telemetry.

Telemetry drain is permitted only outside candidate timing:

```text
end of positive fixture
end of benchmark warmup
end of benchmark bucket
end of canary batch
artifact finalization
```

The API separates:

```text
schedule_guard_decision_telemetry_drain
finish_guard_decision_telemetry_drain_wait
```

A blocking poll is permitted in finalization, but not in the candidate hot path. While a telemetry drain is in flight, new candidate admission is refused instead of appending into a range whose drain snapshot has already been fixed. This is explicit backpressure, not a hidden wait.

Required:

```text
telemetry_overflow_count=0
telemetry_backpressure_count=0
telemetry_drain_failure_count=0
output_value_readback_count=0
```

---

## 9. Persistent ownership

`HeadwiseGuardDecisionRuntime` owns:

```text
guard/decision/downstream pipelines
decision-token slot ring
persistent params/result/token buffers
persistent bind groups
telemetry buffer
device fault latch
slot generation
telemetry scheduling and drain accounting
```

`NativeWgpuModel` owns:

```text
candidate nonce
candidate-output tensor ring
guarded downstream tensor ring
route policy
host telemetry mirror
existing o_proj and residual execution
```

---

## 10. Static truth repair

R12-R2 used a prefix-colliding function-end marker. R12-R3 requires an exact brace-depth extractor:

```text
find exact function signature
find opening brace
increment on {
decrement on }
return when depth returns to zero
```

Static checks must cover:

```text
DeviceGuardDecisionToken runtime exists
fail-closed token initialization exists
dispatch_workgroups_indirect exists in the guarded downstream path
hot-path fused function contains no map_async
hot-path fused function contains no PollType::Wait
model route consumes guarded downstream tensor
host mirror is not authority
R10 kernel revision remains unchanged
```

---

## 11. Performance

Mandatory buckets:

```text
8,16,32,64,128,256,512,1024,2048
```

Measurement:

```text
warmups=128
rounds=32
pairs_per_round=32
pairs_per_bucket=1024
reference-first rounds=16
Atlas-first rounds=16
```

Timed Atlas route includes token and indirect staging dispatch but excludes telemetry mapping and artifact serialization.

Thresholds remain unchanged:

```text
bucket median_ratio<=1.00
bucket p95_ratio<=1.05
paired_regression_probability<=0.05
geometric_mean_median_ratio<=0.95
worst_bucket_median_ratio<=1.00
performance_bucket_fail_count=0
```

---

## 12. Negative controls

R12-R3 re-executes 320 inherited controls and adds 100 controls:

```text
device_decision=25
gpu_downstream_gate=25
async_telemetry=25
static_authority=25
total=420
```

A separate live GPU rejection fixture injects NaN into the Atlas candidate path and requires:

```text
authority_granted=false
indirect dispatch=[0,0,0]
downstream staging remains zero
Atlas commit count=0
explicit reference retry count=1
```

Required aggregate:

```text
negative_control_count=420
negative_control_executed_count=420
negative_control_skipped_count=0
negative_control_fail_count=0
unexpected_failure_code_count=0
```

---

## 13. Source files

```text
crates/burn_webgpu_backend/src/headwise_guard_decision.rs
crates/burn_webgpu_backend/src/headwise_atlas.rs
crates/burn_webgpu_backend/src/headwise_finite_guard.rs
crates/burn_webgpu_backend/src/shaders/headwise_guard_decision_token.wgsl
crates/burn_webgpu_backend/src/shaders/headwise_guarded_downstream_copy.wgsl
crates/burn_webgpu_backend/src/shaders/headwise_atlas_output_finite_guard.wgsl
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/native_wgpu.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/src/bin/ash_attn_headwise_causal_01b_r12_r3_gate.rs
crates/orchestrator_local/Cargo.toml
```

---

## 14. Artifacts

Rust generates under `workspace/runtime/attention/`:

```text
ash_attn_headwise_causal_01b_r12_r3_runtime_artifact.json
ash_attn_headwise_causal_01b_r12_r3_local_manifest.json
ash_attn_headwise_causal_01b_r12_r3_parent_binding_receipt.json
ash_attn_headwise_causal_01b_r12_r3_scope_snapshot.json
ash_attn_headwise_causal_01b_r12_r3_guard_policy_snapshot.json
ash_attn_headwise_causal_01b_r12_r3_guard_ring_policy.json
ash_attn_headwise_causal_01b_r12_r3_guard_ring_creation_receipt.json
ash_attn_headwise_causal_01b_r12_r3_resource_allocation_summary.json
ash_attn_headwise_causal_01b_r12_r3_submission_accounting_summary.json
ash_attn_headwise_causal_01b_r12_r3_poll_mapping_summary.json
ash_attn_headwise_causal_01b_r12_r3_guard_overhead_breakdown.json
ash_attn_headwise_causal_01b_r12_r3_candidate_state_transition_log.json
ash_attn_headwise_causal_01b_r12_r3_guard_dispatch_receipts.json
ash_attn_headwise_causal_01b_r12_r3_candidate_validation_receipts.json
ash_attn_headwise_causal_01b_r12_r3_authority_commit_receipts.json
ash_attn_headwise_causal_01b_r12_r3_fault_injection_matrix.json
ash_attn_headwise_causal_01b_r12_r3_canary_receipt.json
ash_attn_headwise_causal_01b_r12_r3_rollback_fixture_receipt.json
ash_attn_headwise_causal_01b_r12_r3_measurement_plan.json
ash_attn_headwise_causal_01b_r12_r3_measurement_round_receipts.json
ash_attn_headwise_causal_01b_r12_r3_performance_catalog.json
ash_attn_headwise_causal_01b_r12_r3_negative_control_registry.json
ash_attn_headwise_causal_01b_r12_r3_negative_control_outcomes.json
ash_attn_headwise_causal_01b_r12_r3_negative_control_group_summary.json
ash_attn_headwise_causal_01b_r12_r3_static_checks.json
ash_attn_headwise_causal_01b_r12_r3_claim_boundary_receipt.json
ash_attn_headwise_causal_01b_r12_r3_verdict.json
```

Runtime artifacts and manifest are excluded from the source bake.

---

## 15. PASS formula

```text
PASS =
  exact R12-R2 HOLD parent binding
  && parent runtime safety components pass
  && parent performance failure is present
  && brace-depth static extractor passes
  && device token is fail-closed
  && positive candidates grant device authority
  && rejected candidates emit zero indirect workgroups
  && candidate values are not visible downstream on reject
  && hot-path map_async count=0
  && hot-path blocking poll count=0
  && hot-path blocking receive count=0
  && hot-path host decision count=0
  && telemetry overflow/backpressure/drain failure counts=0
  && output value readback count=0
  && all 9 performance buckets pass unchanged thresholds
  && all 420 controls pass
  && artifact digests pass
  && model quality claim count=0
```

---

## 16. Claim boundary

R12-R3 PASS grants:

```text
IncrementalDecode -> AtlasProductionDeviceGuardedStagingScoped
Guard authority -> DeviceGuardDecisionToken
Candidate downstream visibility -> indirect GPU gate
Host guard role -> telemetry mirror only
Hot-path host wait -> forbidden
Output value readback -> forbidden
```

R12-R3 does not prove:

```text
direct o_proj zero-invocation gating
native indirect o_proj matmul
zero telemetry readback
zero host synchronization over the full session
transactional KV rollback
canonical 22-layer decode E2E
full-prefill production
chunked production
model-quality improvement
```

---

## 17. Canonical run

```powershell
$env:CARGO_TARGET_DIR="target-ash-attn-01b-r12-r3"

cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01b_r12_r3_gate `
  -- `
  --repo-root . `
  --parent-artifact workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r2_runtime_artifact.json `
  --parent-manifest workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r2_local_manifest.json `
  --runtime-profile specs/runtime_profile_v5_48259.toml `
  --verdict-scope incremental-only `
  --promote-full-prefill false `
  --promote-incremental-decode true `
  --promote-chunked-decode false `
  --require-same-device true `
  --require-qkv-zero-copy true `
  --require-output-zero-copy true `
  --forbid-output-value-readback true `
  --forbid-output-host-upload true `
  --guard-mode device-native-token `
  --decision-token-ring-capacity 4 `
  --telemetry-ring-capacity 4096 `
  --require-device-native-decision true `
  --require-gpu-gated-o-proj true `
  --require-gpu-gated-residual true `
  --require-zero-hot-path-host-wait true `
  --require-async-telemetry-drain true `
  --guard-workgroup-size 256 `
  --performance-mode paired-gpu-timestamp `
  --warmup-iterations 128 `
  --measurement-pairs 1024 `
  --measurement-rounds 32 `
  --internal-canary-prefills 0 `
  --internal-canary-decode-steps 1024 `
  --fault-injection true `
  --require-rollback true `
  --negative-control-mode executed `
  --minimum-live-negative-controls 40 `
  --expected-negative-controls 420 `
  --require-rollback-anchor true `
  --require-authority-commit-order true `
  --full-source-hash true `
  --out-dir workspace/runtime/attention
```

PASS token:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_DEVICE_NATIVE_GUARD_DECISION_TOKEN_GPU_GATED_DOWNSTREAM_CONSUMPTION_ASYNCHRONOUS_COMPACT_TELEMETRY_DRAIN_ZERO_HOT_PATH_HOST_WAIT_GUARDED_PERFORMANCE_RECOVERY_INCREMENTAL_ONLY_NO_OUTPUT_VALUE_READBACK_NO_PREFILL_PROMOTION_NO_CHUNKED_PROMOTION_NO_TRANSACTIONAL_ROLLBACK_OVERCLAIM_NO_CANONICAL_FULL_DECODE_OVERCLAIM_NO_MODEL_QUALITY_OVERCLAIM
```

HOLD token:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_DEVICE_DECISION_GPU_GATE_ASYNC_TELEMETRY_OR_ZERO_WAIT_RECOVERY_INCOMPLETE
```
