# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R2

## Persistent Guard Resource Ring /
## Single-Wait Compact Resolve /
## Dispatch-Guard Submission Fusion /
## Guarded Performance Recovery Seal

---

## 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R2
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R1
parent_runtime_schema=ash.attn.headwise.causal.01b.r12.runtime_artifact.v1
runtime_schema=ash.attn.headwise.causal.01b.r12.r2.runtime_artifact.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R2
attention_kernel_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
finite_guard_numeric_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R1
guard_runtime_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R2
promotion_scope=incremental_decode_only
attention_math_change=false
finite_classification_change=false
candidate_validation_policy_change=false
authority_commit_policy_change=false
performance_threshold_change=false
```

R12-R2 preserves the R12 finite-guard and authority-ordering contract. It removes per-candidate guard allocation, separate guard submission, and duplicate blocking waits that caused the R12-R1 guarded route to remain HOLD.

---

## 1. Parent HOLD binding

Required parent files:

```text
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_runtime_artifact.json
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_local_manifest.json
```

Required parent state:

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12
build_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R1
pass=false
status=HOLD
production_pass=true
guard_pass=true
canary_pass=true
rollback_fixture_pass=true
static_pass=true
policy_pass=true
negative_control_pass=true
performance_pass=false
failed_components=["guarded_performance_true_round_non_regression"]
```

No parent failure other than guarded performance is admissible. R12-R2 must not relax median, p95, paired-probability, geomean, or worst-bucket thresholds.

---

## 2. Preserved safety contract

```text
Atlas output begins as Candidate.
GPU finite guard completes before commit eligibility.
NaN and positive/negative infinity reject before commit.
Candidate nonce, slot generation, output identity, and element count are revalidated.
Atlas authority commits only from CommitEligible.
o_proj, residual, KV, global cursor, and sampling cannot consume output before commit.
Attention output values never materialize on CPU.
Only compact guard metadata may be read back.
```

Forbidden recovery methods:

```text
guard omission or sampling
N-token guard cadence
delayed next-token validation
optimistic commit before guard resolve
2048-only guard bypass
output-value readback
performance-threshold relaxation
```

---

## 3. SSOT ownership

### `HeadwiseFiniteGuardRuntime`

Owns the guard shader/pipeline, persistent resource ring, slot lifecycle, slot generation, map callback, single blocking poll, unmap, and recycle accounting. It does not own model production authority.

### `HeadwiseAtlasDispatcher`

Owns Q/K/V and output raw leases, attention route selection, attention encoding, guard encoding, the fused command encoder, and the single queue submission. It does not commit model authority.

### `NativeWgpuModel`

Owns the candidate nonce, persistent candidate-output ring, rollback anchor, route admission, candidate validation, `CommitEligible`, `AtlasProductionCommitted`, and downstream `o_proj` permission.

### `GuardSlotLease`

Binds one candidate to one slot generation:

```text
slot_index
slot_generation
candidate_nonce
candidate_digest
device/runtime ownership
```

A lease is non-Clone and non-Copy. A slot cannot become reusable before callback completion, compact-result ownership transfer, unmap, and generation advance.

---

## 4. Persistent guard and output rings

Canonical guard ring:

```text
policy_id=persistent_device_epoch_ring_v1
minimum_capacity=3
default_capacity=4
maximum_capacity=16
canonical_capacity=4
```

Each guard slot persistently owns:

```text
params_buffer
result_buffer
readback_buffer
guard_bind_group
slot state and generation
```

`NativeWgpuModel` owns a four-slot candidate-output ring. The slot is selected by:

```text
slot_index=(candidate_nonce-1)%4
```

The output ring is required because a persistent guard bind group cannot remain truthful if its output-storage binding changes every candidate.

Ring creation or slot rebinding is allowed only during initialization, runtime/device recreation, explicit rebuild, shape change, or benchmark warmup. After warmup:

```text
timed_guard_params_buffer_create_count=0
timed_guard_result_buffer_create_count=0
timed_guard_readback_buffer_create_count=0
timed_guard_bind_group_create_count=0
timed_guard_pipeline_create_count=0
```

---

## 5. Slot lifecycle and stale-result prevention

Canonical lifecycle:

```text
Available
→ Leased
→ Prepared
→ Encoded
→ Submitted
→ MappingRequested
→ Resolved
→ Validated
→ Unmapped
→ Recyclable
→ Available
```

Forbidden:

```text
Submitted → Available
MappingRequested → Available
Resolved → Available
Faulted → Available without explicit reset
reuse before resolve
reuse before unmap
```

The compact result echoes:

```text
slot_index
slot_generation_lo
slot_generation_hi
candidate_nonce_lo
candidate_nonce_hi
```

Required zero counters:

```text
slot_reuse_before_resolve_count=0
slot_reuse_before_unmap_count=0
slot_generation_mismatch_count=0
stale_map_callback_count=0
double_resolve_count=0
double_unmap_count=0
```

---

## 6. Dispatch-guard submission fusion

The encoded attention API accepts an existing `wgpu::CommandEncoder` and must not submit, poll, map, or commit authority. The encoded guard API accepts the same encoder and must not submit, poll, map, or commit authority.

Canonical sequence:

```text
create one command encoder
clear persistent guard result buffer
begin attention compute pass
  dispatch short-KV or long-KV attention
end attention compute pass
begin finite-guard compute pass
  scan exact candidate output buffer
end finite-guard compute pass
copy compact result to persistent readback buffer
finish encoder
queue.submit exactly once
```

Attention and guard use separate compute passes in the same encoder. The pass boundary establishes output-storage write-to-read ordering.

Per candidate:

```text
command_encoder_count=1
queue_submit_count=1
attention_compute_pass_count=1
guard_compute_pass_count=1
compact_result_copy_count=1
separate_guard_submission_count=0
```

---

## 7. Single-wait compact resolve

Forbidden legacy path:

```text
submit → poll(Wait) → map_async → poll(Wait)
```

Required path:

```text
submit fused command buffer
→ map_async compact readback
→ one device.poll(Wait)
→ receive callback
→ copy compact bytes into an owned Rust value
→ unmap
→ recycle slot
```

Per candidate:

```text
map_async_request_count=1
blocking_poll_count=1
pre_map_blocking_poll_count=0
post_map_additional_poll_count=0
map_callback_failure_count=0
unmap_count=1
output_value_bytes_read_back=0
```

No submitted-work wait may be inserted before `map_async`.

---

## 8. Numeric and authority preservation

IEEE-754 masks remain R12-R1 authoritative:

```text
F32_SIGN_MASK=0x80000000
F32_EXPONENT_MASK=0x7f800000
F32_MANTISSA_MASK=0x007fffff
```

Positive guard result:

```text
visited_element_count=expected_element_count
non_finite_count=0
nan_count=0
positive_infinity_count=0
negative_infinity_count=0
max_abs finite and non-negative
```

NaN, positive infinity, negative infinity, and mixed non-finite fixtures must reject before commit.

Authority ordering remains:

```text
CandidateAllocated
→ CandidateDispatched
→ GuardPending
→ GuardCompleted
→ CandidateValidated
→ CommitEligible
→ AtlasProductionCommitted
→ o_proj permitted
```

Required zero counters:

```text
atlas_commit_before_guard_count=0
atlas_commit_before_resolve_count=0
atlas_commit_before_validation_count=0
atlas_commit_before_eligibility_count=0
o_projection_before_commit_count=0
kv_before_commit_count=0
global_cursor_before_commit_count=0
sampling_before_commit_count=0
mixed_authority_count=0
```

---

## 9. Performance gate

The authoritative Atlas route includes slot acquisition, parameter write, one encoder, attention encoding, guard encoding, compact copy, one submission, one map request, one blocking poll, compact validation, candidate validation, authority commit bookkeeping, unmap, and recycle.

Mandatory buckets:

```text
8,16,32,64,128,256,512,1024,2048
```

Canonical measurement:

```text
warmups=128
rounds=32
pairs_per_round=32
pairs_per_bucket=1024
reference_first_rounds=16
atlas_first_rounds=16
```

Unchanged thresholds:

```text
bucket median_ratio<=1.00
bucket p95_ratio<=1.05
paired_regression_probability<=0.05
route geometric_mean_median_ratio<=0.95
worst_bucket_median_ratio<=1.00
performance_bucket_count=9
performance_bucket_fail_count=0
```

Operational gates after warmup:

```text
one encoder, submit, map, blocking poll, and unmap per candidate
zero timed guard resource creation
zero separate guard submission
zero slot reuse violation
```

---

## 10. Negative controls

R12-R2 re-executes 240 R12 controls and adds 80 controls:

```text
persistent_ring=20
resource_allocation=20
submission_fusion=20
single_wait=20
total=320
```

Each new operational control mutates exactly one field in an independently validated all-valid baseline and compares the observed stable failure code with the expected code.

Required aggregate:

```text
negative_control_count=320
negative_control_executed_count=320
negative_control_skipped_count=0
negative_control_fail_count=0
expected_failure_observed_count=320
unexpected_failure_code_count=0
all unintended commit counts=0
```

---

## 11. Source and artifacts

Required source changes:

```text
crates/burn_webgpu_backend/src/headwise_finite_guard.rs
crates/burn_webgpu_backend/src/headwise_atlas.rs
crates/burn_webgpu_backend/src/shaders/headwise_atlas_output_finite_guard.wgsl
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/native_wgpu.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/src/bin/ash_attn_headwise_causal_01b_r12_r2_gate.rs
crates/orchestrator_local/Cargo.toml
```

Rust generates under `workspace/runtime/attention/`:

```text
ash_attn_headwise_causal_01b_r12_r2_runtime_artifact.json
ash_attn_headwise_causal_01b_r12_r2_local_manifest.json
ash_attn_headwise_causal_01b_r12_r2_parent_binding_receipt.json
ash_attn_headwise_causal_01b_r12_r2_scope_snapshot.json
ash_attn_headwise_causal_01b_r12_r2_guard_ring_policy.json
ash_attn_headwise_causal_01b_r12_r2_guard_ring_creation_receipt.json
ash_attn_headwise_causal_01b_r12_r2_resource_allocation_summary.json
ash_attn_headwise_causal_01b_r12_r2_submission_accounting_summary.json
ash_attn_headwise_causal_01b_r12_r2_poll_mapping_summary.json
ash_attn_headwise_causal_01b_r12_r2_guard_overhead_breakdown.json
ash_attn_headwise_causal_01b_r12_r2_candidate_state_transition_log.json
ash_attn_headwise_causal_01b_r12_r2_guard_dispatch_receipts.json
ash_attn_headwise_causal_01b_r12_r2_candidate_validation_receipts.json
ash_attn_headwise_causal_01b_r12_r2_authority_commit_receipts.json
ash_attn_headwise_causal_01b_r12_r2_fault_injection_matrix.json
ash_attn_headwise_causal_01b_r12_r2_negative_control_registry.json
ash_attn_headwise_causal_01b_r12_r2_negative_control_outcomes.json
ash_attn_headwise_causal_01b_r12_r2_negative_control_summary.json
ash_attn_headwise_causal_01b_r12_r2_measurement_plan.json
ash_attn_headwise_causal_01b_r12_r2_measurement_round_receipts.json
ash_attn_headwise_causal_01b_r12_r2_guarded_performance_catalog.json
ash_attn_headwise_causal_01b_r12_r2_static_checks.json
ash_attn_headwise_causal_01b_r12_r2_claim_boundary_receipt.json
ash_attn_headwise_causal_01b_r12_r2_verdict.json
```

Runtime artifacts and the manifest are excluded from the source bake archive.

---

## 12. PASS formula and claim boundary

```text
PASS =
  exact performance-only R12-R1 HOLD binding
  && R12 safety, numeric, validation, and authority obligations preserved
  && persistent ring capacity == 4
  && timed guard resource creation counts == 0
  && slot reuse/generation/stale-callback violations == 0
  && one encoder and one queue submission per candidate
  && one map_async and one blocking poll per candidate
  && no pre-map or post-map extra poll
  && output-value readback count == 0
  && all authority-order violation counts == 0
  && all 9 performance buckets pass unchanged thresholds
  && all 320 negative controls pass
  && static checks and artifact digests pass
  && model_quality_claim_count == 0
```

PASS grants:

```text
IncrementalDecode admitted buckets -> AtlasProductionGuardedScoped
Guard resources -> PersistentRuntimeRing
Guard submission -> AttentionGuardSingleSubmission
Compact resolve -> SingleBlockingWait
Output value readback -> Forbidden
```

It does not prove zero host synchronization, same-device guard decision, zero compact metadata readback, transactional KV rollback, canonical 22-layer decode E2E, full-prefill production, chunked production, or model-quality improvement.

HOLD leaves R11 `AtlasProductionScoped` as the last promoted authority and still emits all R12-R2 artifacts.

---

## 13. Canonical run

```powershell
$env:CARGO_TARGET_DIR="target-ash-attn-01b-r12-r2"

cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01b_r12_r2_gate `
  -- `
  --repo-root . `
  --parent-artifact workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_runtime_artifact.json `
  --parent-manifest workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_local_manifest.json `
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
  --guard-mode compact-async-readback-single-wait `
  --guard-ring-capacity 4 `
  --require-persistent-guard-ring true `
  --require-single-wait-resolve true `
  --require-dispatch-guard-fusion true `
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
  --expected-negative-controls 320 `
  --require-rollback-anchor true `
  --require-authority-commit-order true `
  --full-source-hash true `
  --out-dir workspace/runtime/attention
```

PASS token:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R2_PERSISTENT_GUARD_RESOURCE_RING_SINGLE_WAIT_COMPACT_RESOLVE_DISPATCH_GUARD_SUBMISSION_FUSION_GUARDED_PERFORMANCE_RECOVERY_INCREMENTAL_ONLY_FINITE_GUARD_PRESERVED_AUTHORITY_COMMIT_ORDERING_PRESERVED_NO_OUTPUT_VALUE_READBACK_NO_PREFILL_PROMOTION_NO_CHUNKED_PROMOTION_NO_TRANSACTIONAL_ROLLBACK_OVERCLAIM_NO_MODEL_QUALITY_OVERCLAIM
```

HOLD token:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R2_PERSISTENT_RING_SINGLE_WAIT_FUSION_OR_PERFORMANCE_RECOVERY_INCOMPLETE
```
