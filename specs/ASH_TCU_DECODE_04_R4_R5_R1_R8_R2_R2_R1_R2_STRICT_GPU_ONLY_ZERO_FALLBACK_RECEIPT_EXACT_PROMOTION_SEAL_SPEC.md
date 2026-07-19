# ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R2-R1-R2
# Strict GPU-Only Last-Logits Typestate / Zero Lazy CPU Materialization Call-Graph / Zero Greedy and Legacy Fallback / Policy-Bound Same-Device Raw-Lease Argmax and Sampler Authority / Receipt-Exact Promotion Reducer Seal

- Patch ID: `ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R2-R1-R2_STRICT_GPU_ONLY_LAST_LOGITS_TYPESTATE_ZERO_LAZY_CPU_MATERIALIZATION_CALL_GRAPH_ZERO_GREEDY_AND_LEGACY_FALLBACK_POLICY_BOUND_SAME_DEVICE_RAW_LEASE_ARGMAX_AND_SAMPLER_AUTHORITY_RECEIPT_EXACT_PROMOTION_REDUCER_SEAL`
- Parent: `ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R2-R1-R1`
- Canonical policy ID: `strict_same_device_gpu_last_logits_v2`
- Canonical execution mode: `strict_gpu_only`
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R3`
- R8-R3 authorization: `false`
- R4-R5-R2 authorization: `false`
- Legacy oracle removal: `false`
- Legacy decoder retirement: `false`
- General production apply: `false`

## 1. Purpose

This patch changes strict last-logits enforcement from flag-based prohibition to structural unreachability.

The strict worker must not express, enter, or repair through:

```text
lazy GPU last-row to CPU materialization
GPU tensor to host data to GPU re-upload
GPU argmax failure to CPU greedy argmax
strict sampler failure to legacy GPU sampler
sampled GPU failure to CPU oracle
post-admission environment policy re-resolution
stdout marker presence as promotion authority
```

Canonical authority:

```text
strict selected token authority
=
same-device raw-lease native GPU argmax
+
same-device raw-lease strict multistage GPU sampler
```

No other selected-token authority is promotable.

## 2. Parent Failure Classification

The parent run admitted all 16 strict workers, but completed only 8 and reported:

```text
native_gpu_argmax_count=0
gpu_sampler_selected_count=8
buffer_async_error_count=8
cpu_materialize_executed_count=0
host_upload_fallback_executed_count=0
```

This proves policy inheritance, not call-graph absence.

```text
observed forbidden count=0
is not equivalent to
forbidden path is unreachable
```

## 3. Policy SSOT

The sole authority chain is:

```text
sealed coordinator policy
→ policy digest
→ single-use worker envelope
→ explicit child CLI
→ worker admission receipt
→ NativeWgpuModel-owned policy object
→ generation transaction
→ token authority receipt
→ final reducer
```

Environment variables are compatibility mirrors only. Strict generation must not re-resolve policy from environment after admission.

Canonical policy:

```rust
StrictGpuDecodePolicy {
    policy_id: "strict_same_device_gpu_last_logits_v2",
    require_same_device_raw: true,
    allow_cpu_materialize: false,
    allow_host_upload: false,
    allow_cpu_greedy: false,
    allow_legacy_gpu_sampler: false,
    allow_cpu_oracle: false,
    require_native_gpu_argmax_for_greedy: true,
    require_strict_multistage_sampler: true,
}
```

`NativeWgpuModel` must own the admitted object. A strict worker without it is rejected before generation.

## 4. Strict Typestate

Required state chain:

```text
UnboundWorker
→ StrictPolicyAdmittedWorker
→ StrictGpuModel
→ StrictGpuGenerationTransaction
→ StrictGpuLastLogits
→ StrictGpuTokenChoice
→ CommittedStrictToken
```

Forbidden transitions:

```text
StrictGpuLastLogits → CpuLastLogits
StrictGpuLastLogits → HostUploadedGpuLastLogits
StrictGpuTokenChoice → CpuGreedyChoice
StrictGpuTokenChoice → LegacyGpuFallbackChoice
```

Strict last-logits owns a same-device raw lease and no CPU row:

```rust
struct StrictGpuLastLogits {
    lease: RawWgpuBufferLease,
    bridge: GpuRawBridgeStepTelemetry,
}
```

It must not contain `cpu_row`, host tensor data, a lazy materializer, or a CPU compatibility buffer.

## 5. Strict and Compat Call-Graph Separation

Strict and compatibility selection use separate entrypoints. Strict code must not reach:

```text
ensure_cpu_row_materialized
ensure_cpu_row_materialized_checked
argmax_from_logits_cpu
select_next_token_with_cpu_oracle
bridge_native_tensor_f32_or_fallback
upload_tensor_f32
dispatch_sample_raw_lease_legacy
LegacyFallback
CpuGreedyFallback
```

A strict GPU failure returns HOLD. It must not call compatibility selection.

## 6. Zero Lazy CPU Materialization

Forbidden for strict last-logits and derived reduction tensors:

```text
Tensor::into_data()
Tensor::to_data()
Tensor::into_scalar()
full logits readback
CPU Vec materialization
CPU top-k merge
CPU argmax or max
CPU penalty application
CPU final structure rerank
```

The only permitted readback is a compact GPU-produced result:

```text
GPU selection kernel
→ { token_id, score, status }
→ one owned GpuReadbackLease
```

A CPU materialization attempt is FAIL with zero contribution.

## 7. Same-Device Raw Bridge

Strict code may use only a fail-closed same-device bridge.

Allowed:

```text
bridge_native_tensor_f32_or_fail
```

Forbidden:

```text
bridge_native_tensor_f32_or_fallback
upload_tensor_f32
GPU tensor → host data → new GPU buffer
```

Missing same-device raw lease yields HOLD. `HostUploadFallback` yields FAIL.

## 8. Greedy Authority

The sole strict greedy path is:

```text
StrictGpuLastLogits
→ same-device RawWgpuBufferLease
→ dispatch_argmax_raw_lease
→ compact {token_id, score, status}
→ GpuReadbackLease
→ strict receipt
→ commit
```

Forbidden:

```text
gpu_last_row.argmax(0).into_scalar()
gpu_last_row.max().into_scalar()
CPU argmax
provisional CPU greedy
GPU error to compatibility selection
GPU error to legacy decoder
```

Raw lease absence, argmax unavailability, dispatch failure, `BufferAsyncError`, or device loss before commit yields HOLD with zero contribution. Retry is coordinator-owned and must use a fresh process, model, device, queue, stream, transaction, nonce, and worker token.

## 9. Sampled Authority

The sole strict sampled path is:

```text
StrictGpuLastLogits
→ same-device RawWgpuBufferLease
→ dispatch_sample_raw_lease_strict
→ strict multistage GPU sampler
→ compact selected-token result
→ GpuReadbackLease
→ strict receipt
→ commit
```

Canonical sampler configuration:

```text
parallel_mode=Strict
rollout=MultistageOnly
fallback_on_mismatch=false
fallback_on_topk_overflow=false
allow_legacy_gpu_sampler=false
allow_cpu_oracle=false
```

Forbidden selected-token sources include legacy, legacy fallback, CPU oracle, CPU sampling, host-upload input, and unknown authority. Sampler failure or overflow yields HOLD, never fallback.

## 10. Feature Admission Matrix

| Feature | Strict admission |
|---|---|
| Same-device raw logits lease | Required |
| Native raw-lease argmax | Required for greedy |
| Strict multistage sampler | Required for sampled |
| CPU-only domain adapter | Reject |
| CPU-only final rerank | Reject |
| CPU recent-token selector | Reject |
| Host-upload bridge | Reject |
| Legacy-only sampler | Reject |
| Missing policy object | Reject |
| Warn or permissive mode | Reject |

## 11. Commit Ordering

```text
GPU selection complete
→ compact readback complete
→ readback lease closed
→ receipt constructed
→ receipt validated
→ token committed
```

A token cannot commit before its authority receipt exists. Pre-commit failure aborts the transaction and contributes zero evidence.

## 12. Receipt-Exact Authority

Allowed strict authority enum:

```rust
enum StrictGpuTokenSelectionAuthority {
    NativeGpuArgmaxRawLease,
    StrictMultistageGpuSamplerRawLease,
}
```

No fallback variant is allowed.

Every selected token receives a Rust-generated receipt containing policy identity, route, generation and token indices, token ID, score, authority, raw bridge label, same-device status, forbidden-use booleans, authoritative status, and receipt digest.

Canonical booleans:

```text
same_device_raw=true
cpu_materialized=false
host_upload_used=false
legacy_fallback_used=false
cpu_oracle_used=false
authoritative=true
```

Missing, duplicate, non-authoritative, or digest-mismatched receipt is FAIL.

## 13. Promotion Reducer

Stdout markers are diagnostics only. The Rust reducer aggregates structured receipts and worker summaries.

Required equations:

```text
authoritative_selected_token_count
=
native_gpu_argmax_selected_token_count
+
strict_gpu_sampler_selected_token_count
```

```text
authoritative_selected_token_count
=
same_device_raw_selected_token_count
```

The following must all be zero:

```text
cpu_materialize_attempt_count
cpu_materialize_execution_count
host_upload_attempt_count
host_upload_execution_count
legacy_gpu_fallback_attempt_count
legacy_gpu_fallback_execution_count
cpu_oracle_attempt_count
cpu_oracle_execution_count
unknown_authority_count
missing_receipt_count
duplicate_receipt_count
non_authoritative_commit_count
policy_digest_mismatch_count
device_identity_mismatch_count
raw_lease_identity_mismatch_count
open_readback_lease_count_at_exit
mapped_buffer_count_at_exit
outstanding_submission_count_at_exit
buffer_async_error_count
device_loss_count
uncaptured_gpu_error_count
```

`all_truth_checks_pass` is computed from all policy, call-graph, typestate, authority, receipt, lifecycle, route, and cohort checks. It must not be constant.

## 14. Static Call-Graph Gate

Required strict symbols:

```text
StrictGpuLastLogits
strict_gpu_last_logits
strict_gpu_greedy_choice
strict_gpu_sampled_choice
bridge_last_logits_raw_outcome_strict
dispatch_adjusted_logits_raw_lease_strict
dispatch_sample_raw_lease_strict
```

Forbidden references inside strict functions:

```text
ensure_cpu_row_materialized
argmax_from_logits_cpu
bridge_native_tensor_f32_or_fallback
dispatch_sample_raw_lease_legacy
dispatch_sample_cpu_logits
select_next_token_with_cpu_oracle
.into_scalar()
LegacyFallback
```

The Rust gate emits the static audit artifact.

## 15. Failure Classification

HOLD:

```text
missing same-device lease
GPU argmax or strict sampler unavailable
GPU dispatch failure
BufferAsyncError before commit
device loss before commit
top-k overflow or strict parity mismatch
```

FAIL:

```text
CPU materialization attempted
host upload attempted
legacy fallback attempted
CPU oracle attempted
policy or device identity mismatch
receipt missing, duplicated, or non-authoritative
partial authoritative commit
strict call graph reaches compatibility capability
```

FAIL workers are not automatically retried.

## 16. Negative Matrix

| ID | Injected condition | Required result |
|---|---|---|
| N01 | Policy object missing | Admission FAIL before GPU touch |
| N02 | CLI strict, environment warn | Admission FAIL |
| N03 | Policy digest mismatch | Admission FAIL |
| N04 | Same-device lease unavailable | HOLD, CPU attempt 0 |
| N05 | Raw lease device mismatch | FAIL |
| N06 | Greedy argmax unavailable | HOLD, greedy fallback 0 |
| N07 | Greedy readback BufferAsyncError | HOLD, CPU fallback 0 |
| N08 | Strict sampler error | HOLD, legacy fallback 0 |
| N09 | Strict sampler top-k overflow | HOLD, legacy fallback 0 |
| N10 | Only host-upload bridge available | HOLD, host upload 0 |
| N11 | CPU-only selected-token feature enabled | Admission FAIL |
| N12 | Duplicate or missing receipt | FAIL |
| N13 | Environment flags changed after admission | No effect |
| N14 | Compat selector canary panic | Strict smoke unaffected |

## 17. Worker Matrix and Smoke Budget

Routes:

```text
greedy_cached
sampled_cached
greedy_streaming
sampled_streaming
```

Cohorts:

```text
legacy_only
full_dual
bounded_reduced
```

Required topology:

```text
4 route workers + 3 cohorts × 4 routes = 16 isolated workers
```

Each route must complete at least 100 generations and 2500 authoritative selected tokens. Greedy receipts must equal greedy selected tokens. Strict sampler receipts must equal sampled selected tokens.

## 18. Rust-Owned Artifacts

All runtime artifacts and manifests are emitted by Rust. Python, PowerShell, shell, JavaScript, and external artifact generators are not promotion authority.

Final paths:

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r5_r1_r8_r2_r2_r1_r2_runtime_artifact.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r5_r1_r8_r2_r2_r1_r2_local_manifest_latest.json
```

Supporting paths:

```text
workspace/runtime/tensorcube/soak/r4_r5_r1_r8_r2_r2_r1_r2/policy_epoch.json
workspace/runtime/tensorcube/soak/r4_r5_r1_r8_r2_r2_r1_r2/strict_callgraph_audit.json
workspace/runtime/tensorcube/soak/r4_r5_r1_r8_r2_r2_r1_r2/workers/<worker_id>/worker_policy_envelope.json
workspace/runtime/tensorcube/soak/r4_r5_r1_r8_r2_r2_r1_r2/workers/<worker_id>/worker_policy_admission.json
workspace/runtime/tensorcube/soak/r4_r5_r1_r8_r2_r2_r1_r2/workers/<worker_id>/worker_summary.json
workspace/runtime/tensorcube/soak/r4_r5_r1_r8_r2_r2_r1_r2/workers/<worker_id>/generation_*_strict_token_receipts.json
```

## 19. PASS Conditions

```text
strict_worker_admission_count=16
worker_process_count=16
worker_success_count=16
worker_hold_count=0
worker_fail_count=0
```

Both authority equations must hold, all forbidden counters must be zero, all truth fields must be true, and route/cohort smoke must pass.

PASS authority:

```text
r4_r5_r1_r8_r2_r2_r1_r2_strict_gpu_only_pass=true
r4_r5_r1_r8_r2_r3_authorized=true
```

Still false:

```text
r4_r5_r1_r8_r3_authorized=false
decode04_r4_r5_r2_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
general_production_apply_authorized=false
```

## 20. Verdict Markers

```text
PASS_ASH_TCU_DECODE_04_R4_R5_R1_R8_R2_R2_R1_R2_STRICT_GPU_ONLY_LAST_LOGITS_TYPESTATE_ZERO_FALLBACK_SEAL
HOLD_ASH_TCU_DECODE_04_R4_R5_R1_R8_R2_R2_R1_R2_STRICT_GPU_ONLY_LAST_LOGITS_TYPESTATE_ZERO_FALLBACK_SEAL
FAIL_ASH_TCU_DECODE_04_R4_R5_R1_R8_R2_R2_R1_R2_STRICT_GPU_ONLY_INVARIANT_VIOLATION
```

## 21. Canonical Binary

```text
ash_tcu_decode_04_r4_r5_r1_r8_r2_r2_r1_r2_strict_gpu_only_last_logits_typestate_zero_fallback_receipt_exact_promotion_gate
```

## 22. Non-Goals

This patch does not delete compatibility CPU decode, the legacy decoder, or the legacy GPU sampler. It isolates strict promotion candidates from them. It does not authorize general production apply or legacy retirement.

## 23. Canonical Seal Statement

```text
Strict decode authority is not defined by a disabled fallback flag.
It is defined by the absence of fallback-capable states, symbols,
transitions, and receipts from the strict call graph.

A failed authorized GPU selection returns HOLD with zero contribution.
An attempted CPU, host-upload, oracle, or legacy repair returns FAIL.
```
