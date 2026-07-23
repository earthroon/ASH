# ASH-ATTN-HEADWISE-CAUSAL-01B

## Shadow-to-Production Authority Promotion /
## KV Lifecycle Binding /
## Performance Non-Regression /
## Rollback Seal

---

# 0. Patch identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B
patch_class=headwise_atlas_production_authority_kv_lifecycle_performance_rollback
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01A
parent_runtime_schema=ash.attn.headwise.causal.01a.runtime_artifact.v1
parent_primary_artifact=workspace/runtime/attention/ash_attn_headwise_causal_01a_runtime_artifact.json
parent_manifest=workspace/runtime/attention/ash_attn_headwise_causal_01a_local_manifest.json
runtime_schema=ash.attn.headwise.causal.01b.runtime_artifact.v1
primary_artifact=workspace/runtime/attention/ash_attn_headwise_causal_01b_runtime_artifact.json
local_manifest=workspace/runtime/attention/ash_attn_headwise_causal_01b_local_manifest.json
promotion_scope=full_prefill_and_incremental_decode_exact_routes
chunked_route_scope=qualified_shadow_only
production_default_change=explicit_model_instance_policy_only
global_repository_default_change=false
```

01B consumes the final local PASS evidence from 01A R9. It promotes only exact, admitted headwise-atlas routes from shadow parity authority to model-instance-bound production output authority.

01B does not treat a successful 01A parity run as sufficient production evidence. Production promotion additionally requires:

```text
same-device dispatcher construction
GPU-resident output ownership
zero CPU readback
zero host re-upload
KV lifecycle position binding
exact route admission
pipeline/cache readiness
paired performance non-regression
single-owner output commit
explicit rollback readiness
```

---

# 1. Parent binding

## 1.1 Required parent files

The gate must load:

```text
workspace/runtime/attention/ash_attn_headwise_causal_01a_runtime_artifact.json
workspace/runtime/attention/ash_attn_headwise_causal_01a_local_manifest.json
```

The parent is accepted only when every required field is present and exact:

```text
schema=ash.attn.headwise.causal.01a.runtime_artifact.v1
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01A
pass=true
route_pass=true
poison_pass=true
static_pass=true
parallel_group_map_pass=true
negative_control_count>=96
negative_fail_count=0
unknown_shader_variant_count=0
future_key_visit_count=0
max_pass_sum_pass_bound_mismatch_count=0
production_authority_claim_count=0
model_quality_claim_count=0
parity_policy_id=atol_plus_rtol_reference_floor_v1
```

The manifest digest must bind the exact parent primary artifact and all required 01A receipts.

## 1.2 Parent claims inherited

01B may inherit only these claims:

```text
absolute query-position SSOT exists
KV visibility upper bound is causal
prefill/incremental/chunked parity fixtures pass
future-key poison controls pass
GQA group map is exact
max-pass and sum-pass share one visibility bound
active shader variant is known
text-density behavior is frozen
```

01B may not inherit:

```text
production authority
same-device output ownership
zero-copy output handoff
performance non-regression
KV lifecycle production binding
rollback safety
```

Those are new 01B obligations.

---

# 2. Confirmed current blockers

The R9 source tree contains the following production blockers.

## 2.1 Separate-device dispatcher construction

The model currently creates the headwise dispatcher through:

```text
HeadwiseAtlasDispatcher::try_new_default()
```

That constructor requests a new adapter/device/queue and is not bound to the model's existing Burn/WGPU runtime handles.

Production use of `try_new_default()` is forbidden.

## 2.2 CPU readback output path

The model currently calls:

```text
dispatch_native_qkv_to_cpu_f32
```

which performs:

```text
GPU headwise output
-> COPY_SRC readback buffer
-> MAP_READ
-> Vec<f32>
```

Production use of this path is forbidden.

## 2.3 Host re-upload

The model currently converts the CPU vector through:

```text
Tensor::from_data
```

which creates a new backend tensor and re-uploads attention output.

Production use of this path is forbidden.

## 2.4 Incremental decode route is not bound

The model helper currently admits only:

```text
seq_q == seq_kv
```

and creates a `FullPrefill` position snapshot with zero bases.

Canonical incremental decode has:

```text
seq_q=1
seq_kv=past_len+1
```

and therefore currently falls back to the reference grouped-query attention path.

## 2.5 Pipeline construction is per dispatch

The current dispatcher creates shader module, bind-group layout, pipeline layout, and compute pipeline during dispatch.

Production promotion requires device-epoch-scoped caching.

---

# 3. Goals

01B must prove all of the following:

```text
01A parent evidence bound exactly
headwise dispatcher uses model's existing device and queue
Q/K/V/output all belong to one device epoch
output tensor is allocated on the native backend
headwise shader writes directly into that tensor's storage
CPU output readback count=0
host output upload count=0
incremental decode receives explicit KV cursor position truth
prefill receives explicit KV lifecycle position truth
chunked route remains non-production unless a real consumer is bound
reference attention production authority is revoked for admitted routes
headwise atlas commits exactly one production output
mixed authority count=0
pipeline cache is hot before timed production evidence
paired release-mode performance does not regress
rollback is possible before downstream output consumption
a rollback never appends KV twice
no silent fallback occurs
```

---

# 4. Non-goals

01B does not:

```text
promote every headwise shader variant
promote chunked decode without a real runtime consumer
change Q/K/V projection weights
change GQA topology
change causal visibility math
change softmax math
change text-density semantics
change sampling
change vocabulary projection
change FFN or GEMM ownership
claim hardware Tensor Core use
claim language-quality improvement
claim translation-quality improvement
change repository-wide replacement default
```

---

# 5. Production authority model

## 5.1 Authority modes

Add:

```rust
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub enum HeadwiseAttentionAuthorityMode {
    ReferenceProduction,
    AtlasShadow,
    AtlasCandidatePrepared,
    AtlasInternalCanary,
    AtlasProduction,
    AtlasRolledBack,
    AtlasQuarantined,
}
```

## 5.2 Route identity

Add:

```rust
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub struct HeadwiseAttentionProductionRouteId {
    pub route_kind: HeadwiseCausalRouteId,
    pub batch: u32,
    pub q_heads: u32,
    pub kv_heads: u32,
    pub head_dim: u32,
    pub sequence_bucket: String,
    pub shader_digest: String,
    pub parallel_group_map_digest: String,
    pub position_abi_digest: String,
}
```

The route digest binds every field.

## 5.3 Model-instance policy snapshot

Add:

```rust
pub struct HeadwiseAttentionPromotionPolicySnapshot {
    pub schema: String,
    pub mode: HeadwiseAttentionAuthorityMode,
    pub model_instance_id: String,
    pub effective_runtime_binding_digest: String,
    pub device_identity_digest: String,
    pub device_epoch: u64,
    pub parent_01a_artifact_digest: String,
    pub parent_01a_manifest_digest: String,
    pub admitted_route_digests: Vec<String>,
    pub reference_rollback_route_digest: String,
    pub operator_authorization_digest: String,
    pub performance_catalog_digest: String,
    pub rollback_policy_digest: String,
    pub semantic_digest: String,
}
```

Ownership:

```text
owner=NativeWgpuModel instance
construction=model load or explicit verified activation
mutability=immutable during one decode session
repository global singleton=forbidden
```

A decode session binds one snapshot at session start. Route authority may not silently change mid-session.

## 5.4 Exact route states

01B route states are:

```text
FullPrefill:
  eligible for AtlasProduction after all 01B gates

IncrementalDecode:
  eligible for AtlasProduction after all 01B gates

ChunkedDecode:
  AtlasShadow / QualifiedCandidate only
  production commit count must remain 0 in 01B
```

A later patch may promote chunked decode only after binding a real chunked runtime consumer.

---

# 6. Same-device dispatcher binding

## 6.1 Required constructor

Add a constructor equivalent to:

```rust
pub fn from_runtime_handles(
    handles: SameDeviceRuntimeHandles,
    device_epoch: u64,
) -> Result<Self>
```

The constructor must use the exact device/queue already owned by `NativeWgpuModel`.

Forbidden in production:

```text
HeadwiseAtlasDispatcher::try_new_default
request_adapter
request_device
new independent queue
new independent device
```

## 6.2 Device identity receipt

Every production dispatch records:

```text
model_device_identity_digest
runtime_handles_device_identity_digest
dispatcher_device_identity_digest
q_buffer_device_identity_digest
k_buffer_device_identity_digest
v_buffer_device_identity_digest
output_buffer_device_identity_digest
device_epoch
all_device_identities_equal
```

PASS requires:

```text
all_device_identities_equal=true
```

## 6.3 Device loss

A device-loss event invalidates:

```text
promotion policy snapshot
pipeline cache
group-map buffer cache
parameter buffer ring
output workspace leases
active production route
```

The old device epoch may never be reused.

---

# 7. GPU-resident output ownership

## 7.1 Allocation owner

The output tensor must be allocated by `NativeInferenceBackend` with logical shape:

```text
[batch, q_heads, seq_q, head_dim]
```

The model obtains a same-device raw buffer lease for that tensor and passes it to the headwise dispatcher as the shader output target.

Required API shape:

```rust
pub fn dispatch_native_qkv_into_tensor(
    &self,
    q: &Tensor<InferenceBackend, 4>,
    k: &Tensor<InferenceBackend, 4>,
    v: &Tensor<InferenceBackend, 4>,
    output: &Tensor<InferenceBackend, 4>,
    spec: &HeadwiseAtlasRuntimeSpec,
) -> Result<HeadwiseAtlasProductionDispatchReceipt>
```

The function returns a receipt, not a CPU vector.

## 7.2 Buffer identity invariant

Required identities:

```text
allocated_output_tensor_primitive_id
allocated_output_buffer_id
headwise_shader_output_buffer_id
returned_tensor_primitive_id
o_projection_input_tensor_primitive_id
```

PASS requires:

```text
allocated_output_tensor_primitive_id == returned_tensor_primitive_id
allocated_output_buffer_id == headwise_shader_output_buffer_id
returned_tensor_primitive_id == o_projection_input_tensor_primitive_id
```

## 7.3 Forbidden output operations

Production dispatch must report:

```text
output_cpu_readback_count=0
output_map_read_count=0
output_copy_to_readback_count=0
output_host_upload_count=0
output_tensor_from_data_count=0
output_cpu_vector_materialization_count=0
```

The shader output may not be copied into a second production tensor.

## 7.4 Buffer usage

Production output buffer usage must include the storage usage needed by the shader and the backend usage needed by downstream tensor operations.

`MAP_READ` is forbidden.

`COPY_SRC` is allowed only in an explicitly separate shadow/parity allocation and may not be present solely to support the production path.

---

# 8. Q/K/V active seam requirement

01A allowed fixtures that were not zero-copy. 01B production does not.

Every production dispatch requires:

```text
q_raw_borrow_count=1
k_raw_borrow_count=1
v_raw_borrow_count=1
q_metadata_only_count=0
k_metadata_only_count=0
v_metadata_only_count=0
q_host_bridge_count=0
k_host_bridge_count=0
v_host_bridge_count=0
active_tensor_zero_copy=true
```

If any seam cannot be borrowed on the same device:

```text
candidate dispatch is not executed
production output is not committed
explicit rollback decision is recorded
```

---

# 9. KV lifecycle SSOT

## 9.1 KV cache fields

Extend `KvCache` with explicit lifecycle truth:

```rust
pub struct KvPositionLifecycle {
    pub decode_session_id: String,
    pub model_instance_id: String,
    pub device_identity_digest: String,
    pub position_epoch: u64,
    pub absolute_position_base: u64,
    pub committed_past_len: usize,
    pub staged_append_len: usize,
    pub next_write_position: u64,
    pub lifecycle_digest: String,
}
```

`KvCache` owns one lifecycle snapshot.

Each `KvLayerCache` records:

```text
layer_id
position_epoch
committed_used_tokens
staged_used_tokens
key_buffer_identity
value_buffer_identity
```

## 9.2 No shape-derived position authority

Forbidden:

```text
q base inferred from seq_kv-seq_q
past length inferred only from tensor shape
position epoch inferred from generation count
route inferred only from seq_q
```

Tensor shapes may be checked against the KV lifecycle snapshot, but may not own position truth.

## 9.3 Layer consistency

Before every attention dispatch:

```text
all layers share one position_epoch
all layers committed_used_tokens == kv.committed_past_len
all key/value sequence lengths agree
all layer bindings match model/session/device
```

A mismatch fails before production dispatch.

---

# 10. Prefill lifecycle binding

Canonical prefill inputs:

```text
route=FullPrefill
seq_q=prompt_len
seq_kv=prompt_len
q_position_base=kv.absolute_position_base
kv_position_base=kv.absolute_position_base
committed_past_len_before=0
staged_append_len=prompt_len
next_committed_past_len=prompt_len
```

Execution order:

```text
1. create prefill KV lifecycle staging snapshot
2. compute Q/K/V
3. validate all layer shapes and device identities
4. dispatch headwise atlas into GPU-resident output tensor
5. commit attention output authority
6. complete layer output
7. commit layer K/V cache tensors
8. after all layers succeed, commit kv.committed_past_len=prompt_len
```

If any layer fails, the prefill KV lifecycle must not claim a partially committed sequence.

---

# 11. Incremental decode lifecycle binding

Canonical decode-step inputs, where `N` is committed past length before the step:

```text
route=IncrementalDecode
seq_q=1
seq_kv=N+1
q_position_base=kv.absolute_position_base+N
kv_position_base=kv.absolute_position_base
committed_past_len_before=N
staged_append_len=1
kv_write_position=kv.absolute_position_base+N
next_committed_past_len=N+1
```

The current token's K/V rows are staged by concatenating or writing into the candidate cache. They are not committed to `KvCache` until attention and the layer complete.

Required invariants:

```text
query absolute position == staged KV append position
visible_count == N+1
read range includes past rows and current staged row
future key visit count=0
layer used_tokens before=N
layer staged used_tokens=N+1
layer committed used_tokens after=N+1
```

The model helper must receive a `HeadwiseCausalPositionSnapshot` or a stronger KV lifecycle-derived position context. It may not reject incremental decode merely because `seq_q != seq_kv`.

---

# 12. Chunked route boundary

01A proved chunked causal parity fixtures. 01B does not have evidence of a canonical production chunked consumer.

Therefore:

```text
chunked shadow dispatch allowed=true
chunked performance measurement allowed=true
chunked production output commit allowed=false
chunked production authority claim count=0
```

Any attempt to commit chunked atlas output in 01B is a contract failure.

---

# 13. Output authority two-phase commit

## 13.1 Candidate phase

The atlas dispatch produces a candidate output tensor and receipt.

During candidate phase:

```text
candidate_output_exists=true
production_output_owner=None
reference_output_commit_count=0
atlas_output_commit_count=0
downstream_o_projection_started=false
KV lifecycle commit=false
```

## 13.2 Commit phase

The candidate becomes authoritative only after:

```text
route admitted
policy snapshot valid
same-device checks pass
causal position checks pass
parallel group map checks pass
dispatch submission succeeds
output identity checks pass
GPU finite-value guard passes
rollback anchor is available
```

Then exactly one commit record is written:

```text
production_output_owner=HeadwiseAtlasProduction
atlas_output_commit_count=1
reference_output_commit_count=0
mixed_output_commit_count=0
```

Only after this commit may the output tensor flow into reshape and `o_proj`.

## 13.3 Reference authority revocation

For an admitted production route:

```text
reference production compute count=0
reference production commit count=0
```

Reference attention may run only as:

```text
explicit benchmark baseline
explicit shadow parity canary
explicit rollback execution
```

Each purpose has a separate receipt and may not silently commit.

---

# 14. GPU finite-value guard

Production promotion requires a GPU-side guard over the atlas output before commit.

Required values:

```text
non_finite_count
max_abs_value
output_element_count
```

The guard may use a compact reduction buffer, but production output values may not be copied to CPU.

Only the compact guard receipt may be read back during the gate. In canonical production runtime, asynchronous device telemetry or a same-device guard decision is preferred.

PASS:

```text
non_finite_count=0
max_abs_value is finite
output_element_count matches logical shape
```

---

# 15. Pipeline and resource cache

## 15.1 Device-epoch cache

Cache once per device epoch:

```text
shader module
bind-group layout
pipeline layout
compute pipeline
```

## 15.2 Plan cache

Cache by exact `HeadwiseAtlasPlanKey`:

```text
parallel group map
group-map GPU buffer
static dispatch geometry
```

## 15.3 Session workspace

A session may own reusable:

```text
parameter buffer ring
text-density uniform buffer ring
finite-guard buffer
output workspace where backend semantics permit
```

## 15.4 Timed-route prohibitions

During timed production measurements:

```text
shader module creation count=0
pipeline creation count=0
bind-group layout creation count=0
group-map upload count=0
adapter request count=0
device request count=0
CPU readback count=0
host upload count=0
```

A bind group may be created per dispatch if dynamic raw buffer identities require it, but that cost must remain inside end-to-end route timing and be receipted.

---

# 16. Performance route catalog

## 16.1 Canonical topology

Mandatory topology:

```text
batch=1
q_heads=32
kv_heads=4
head_dim=64
query_heads_per_kv=8
```

## 16.2 Full-prefill buckets

Mandatory sequence lengths:

```text
8,16,32,64,128,256,512,1024
```

`2048` is mandatory when supported by the runtime profile and available memory.

## 16.3 Incremental-decode buckets

Mandatory committed KV lengths before append:

```text
7,15,31,63,127,255,511,1023,2047
```

The dispatched `seq_kv` values are therefore:

```text
8,16,32,64,128,256,512,1024,2048
```

## 16.4 Bucket authority

Performance admission is bucket-specific.

A bucket not meeting the threshold remains `ReferenceProduction` and may not be silently routed to atlas.

A route-wide atlas mode may be claimed only when every mandatory bucket passes.

---

# 17. Performance measurement protocol

## 17.1 Build and environment

Required:

```text
cargo profile=release
debug_assertions=false
GPU timestamp query supported=true
same adapter/device for baseline and candidate
shader digest fixed
pipeline cache warmed
power/thermal drift monitored
```

CPU wall-clock timing may be supplemental but cannot own the performance verdict.

## 17.2 Paired ordering

For every bucket:

```text
warmup iterations per route >=128
measurement pairs >=1024
round count >=32
alternating order:
  odd round: Reference then Atlas
  even round: Atlas then Reference
```

No readback occurs in the timed region.

## 17.3 Timing scopes

Record both:

```text
kernel_gpu_ns
attention_route_gpu_ns
```

`attention_route_gpu_ns` includes:

```text
parameter preparation
same-device raw lease validation
bind-group creation when applicable
dispatch
finite guard
authority commit bookkeeping required by the route
```

It excludes unrelated Q/K/V projection and `o_proj` unless an additional end-to-end measurement explicitly includes them.

## 17.4 End-to-end metrics

Also measure:

```text
prefill attention contribution to TTFT
decode attention contribution to per-token latency
full prompt-to-token latency smoke
```

---

# 18. Performance thresholds

For each mandatory bucket, define:

```text
median_ratio = atlas_median / reference_median
p95_ratio = atlas_p95 / reference_p95
```

Bucket PASS requires:

```text
median_ratio <= 1.00
p95_ratio <= 1.05
paired_regression_probability <= 0.05
thermal_drift_hold=false
```

Route-wide promotion additionally requires:

```text
geometric_mean_median_ratio <= 0.95
worst_mandatory_bucket_median_ratio <= 1.00
end_to_end_p50_ratio <= 1.00
end_to_end_p95_ratio <= 1.03
```

Interpretation:

```text
no mandatory bucket may regress at the median
route-wide atlas promotion requires at least 5% geometric-mean improvement
p95 allows at most 5% bucket noise and 3% end-to-end noise
```

If only a subset passes, only those exact buckets may be promoted.

---

# 19. Parity and production canary

## 19.1 Promotion-time parity

Every admitted bucket must re-run 01A parity under the production same-device output path.

Required:

```text
parity_policy_id=atol_plus_rtol_reference_floor_v1
mismatch_element_count=0
non_finite_count=0
max_tolerance_ratio<=1.0
future_key_visit_count=0
bound_mismatch_count=0
```

## 19.2 Internal canary

Before full model-instance production, run an internal canary over:

```text
at least 128 prefill operations
at least 1024 incremental decode steps
multiple prompt lengths
multiple seeds
```

The reference path may run as shadow only for selected canary steps.

Canary output may not replace atlas output unless rollback is explicitly triggered.

## 19.3 Production sentinel

A production session may use a sparse sentinel policy, for example:

```text
first prefill
first decode step
powers-of-two decode positions
final configured sentinel step
```

The sentinel must not require full CPU output materialization.

---

# 20. Rollback policy

## 20.1 Rollback modes

Add:

```rust
pub enum HeadwiseAttentionRollbackMode {
    FailClosed,
    SingleReferenceRetryBeforeCommit,
}
```

Canonical 01B production policy:

```text
SingleReferenceRetryBeforeCommit
```

## 20.2 Eligible rollback points

Current-step rollback is allowed only before:

```text
atlas production output commit
o_projection consumption
layer residual commit
KV layer cache commit
global kv.past_len increment
sampling/token commit
```

## 20.3 Rollback execution

On an eligible failure:

```text
1. mark atlas candidate rejected
2. preserve the same Q/K/V candidate tensors
3. execute reference grouped-query attention exactly once
4. commit reference output exactly once
5. commit the staged K/V cache exactly once
6. demote atlas route for the remainder of the session
7. append rollback ledger record
```

Forbidden:

```text
second KV append
second token generation
second sampling call
mixed atlas/reference output
silent fallback
retry loop
more than one reference retry
```

## 20.4 Post-commit failure

If a critical error is detected after atlas output commit:

```text
current step may not be silently recomputed
session enters fail-closed or quarantine state
token commit is blocked when still possible
operator-visible receipt is required
```

## 20.5 Session demotion

After rollback:

```text
mode=AtlasRolledBack
atlas production dispatch count for later steps=0
reference production route active for remainder of session
session rollback epoch increments exactly once
```

A later session requires a fresh promotion-policy binding.

---

# 21. Rollback ledger

Add:

```rust
pub struct HeadwiseAttentionRollbackReceipt {
    pub receipt_id: String,
    pub decode_session_id: String,
    pub model_instance_id: String,
    pub route_digest: String,
    pub layer_id: usize,
    pub decode_phase: String,
    pub decode_step: usize,
    pub failure_kind: String,
    pub failure_stage: String,
    pub failure_before_output_commit: bool,
    pub reference_retry_allowed: bool,
    pub reference_retry_executed: bool,
    pub atlas_output_commit_count: u32,
    pub reference_output_commit_count: u32,
    pub kv_append_count: u32,
    pub sampling_commit_count: u32,
    pub session_demoted: bool,
    pub quarantine_required: bool,
    pub previous_policy_digest: String,
    pub next_policy_digest: String,
    pub receipt_digest: String,
}
```

PASS rollback fixture requires:

```text
reference_retry_executed=true
atlas_output_commit_count=0
reference_output_commit_count=1
kv_append_count=1
sampling_commit_count=0 at attention rollback boundary
session_demoted=true
```

---

# 22. Production dispatch receipt

Add:

```rust
pub struct HeadwiseAtlasProductionDispatchReceipt {
    pub dispatch_id: String,
    pub route_digest: String,
    pub policy_digest: String,
    pub model_instance_id: String,
    pub decode_session_id: String,
    pub device_identity_digest: String,
    pub device_epoch: u64,
    pub layer_id: usize,
    pub decode_phase: String,
    pub decode_step: usize,
    pub q_position_base: u64,
    pub kv_position_base: u64,
    pub position_epoch: u64,
    pub seq_q: u32,
    pub seq_kv: u32,
    pub kv_committed_len_before: usize,
    pub kv_staged_append_len: usize,
    pub kv_committed_len_after: usize,
    pub parallel_group_count: u32,
    pub dispatch_x: u32,
    pub dispatch_y: u32,
    pub dispatch_z: u32,
    pub q_zero_copy: bool,
    pub k_zero_copy: bool,
    pub v_zero_copy: bool,
    pub output_zero_copy: bool,
    pub output_buffer_identity_match: bool,
    pub pipeline_cache_hit: bool,
    pub group_map_cache_hit: bool,
    pub output_cpu_readback_count: u32,
    pub output_host_upload_count: u32,
    pub non_finite_count: u32,
    pub candidate_prepared: bool,
    pub atlas_output_committed: bool,
    pub reference_output_committed: bool,
    pub rollback_executed: bool,
    pub mixed_authority_count: u32,
    pub receipt_digest: String,
}
```

---

# 23. Failure classification

Required failure kinds:

```text
Parent01AArtifactMissing
Parent01AManifestMissing
Parent01ADigestMismatch
Parent01ANotPass
PromotionPolicyMissing
PromotionPolicyDigestMismatch
RouteNotAdmitted
RouteBucketNotAdmitted
ChunkedProductionCommitForbidden
ModelInstanceBindingMismatch
DecodeSessionBindingMismatch
DeviceIdentityMismatch
DeviceEpochMismatch
IndependentDispatcherDeviceObserved
QRawLeaseUnavailable
KRawLeaseUnavailable
VRawLeaseUnavailable
OutputRawLeaseUnavailable
OutputBufferIdentityMismatch
OutputCpuReadbackObserved
OutputHostUploadObserved
OutputTensorFromDataObserved
KvLifecycleMissing
KvPositionEpochMismatch
KvLayerCursorMismatch
KvStagedAppendMismatch
IncrementalPositionMismatch
FutureKeyVisitObserved
SoftmaxBoundMismatch
ParallelGroupMapMismatch
PipelineCacheColdInTimedRegion
PipelineCreatedInTimedRegion
GroupMapUploadedInTimedRegion
NonFiniteOutputObserved
ParityMismatch
PerformanceRegression
PerformanceTimestampUnavailable
ThermalDriftHold
AtlasCommitBeforeValidation
ReferenceAuthorityNotRevoked
MixedAuthorityObserved
RollbackAnchorMissing
RollbackAfterCommitAttempted
RollbackReferenceRetryCountInvalid
RollbackKvDoubleAppend
RollbackSessionDemotionMissing
SilentFallbackObserved
```

---

# 24. Negative controls

Minimum 160 controls, grouped as:

```text
20 parent-binding controls
20 device-identity controls
20 output-ownership controls
20 KV-lifecycle controls
20 route-authority controls
20 performance controls
20 rollback controls
20 receipt/static controls
```

Required examples:

```text
01A artifact digest changed
01A pass=false
manifest omits parity receipt
dispatcher created with try_new_default
Q device differs from model device
output device differs from Q/K/V
output tensor primitive differs after dispatch
CPU readback count=1
host upload count=1
Tensor::from_data observed in production helper
incremental q base off by one
incremental seq_kv remains N instead of N+1
layer used_tokens disagree
position epoch differs on one layer
chunked production commit attempted
reference and atlas both commit
atlas commits before finite guard
pipeline created in timed region
GPU timestamp unsupported
median regression above threshold
p95 regression above threshold
rollback invoked after o_proj consumed output
rollback executes reference twice
rollback appends KV twice
rollback leaves atlas active
silent fallback without ledger
```

Every negative control must prove the intended failure code and zero unintended production commits.

---

# 25. Static checks

Static checks must be symbol-scoped or function-body scoped.

Required checks:

```text
production model constructor does not call HeadwiseAtlasDispatcher::try_new_default
production dispatcher is built from existing runtime handles
production attention helper does not call dispatch_native_qkv_to_cpu_f32
production attention helper does not call dispatch_prepared_to_cpu_f32
production attention helper does not call readback_output_f32
production attention helper does not call Tensor::from_data for atlas output
incremental path constructs explicit IncrementalDecode position snapshot
prefill path constructs explicit FullPrefill position snapshot
KV lifecycle snapshot is passed into the attention helper
chunked production commit path is absent or guarded false
pipeline creation is outside the dispatch hot function
parallel group map remains KV-head-owned
text-density function digest remains unchanged
causal shader digest binds the 01A-compatible visibility rule
```

Comments, logs, tests, receipt field names, and specification text are excluded from executable-code counts.

---

# 26. Runtime gate

Add a new bin with a new binary identity:

```text
crates/orchestrator_local/src/bin/ash_attn_headwise_causal_01b_gate.rs
```

The gate must:

```text
load and validate 01A primary artifact and manifest
bootstrap the existing model device
construct headwise dispatcher from existing runtime handles
bind a verified model-instance promotion policy
run same-device output ownership tests
run prefill KV lifecycle production smoke
run incremental KV lifecycle production smoke
run chunked non-production guard
run parity under the production zero-copy output path
warm all caches
run paired GPU timestamp benchmarks
run internal canary
run rollback fault-injection matrix
run negative controls
emit receipts and verdict
```

---

# 27. Required artifacts

```text
workspace/runtime/attention/
  ash_attn_headwise_causal_01b_runtime_artifact.json
  ash_attn_headwise_causal_01b_local_manifest.json
  ash_attn_headwise_causal_01b_parent_binding_receipt.json
  ash_attn_headwise_causal_01b_promotion_policy_snapshot.json
  ash_attn_headwise_causal_01b_device_identity_receipt.json
  ash_attn_headwise_causal_01b_output_ownership_receipt.json
  ash_attn_headwise_causal_01b_qkv_seam_receipt.json
  ash_attn_headwise_causal_01b_kv_lifecycle_matrix.json
  ash_attn_headwise_causal_01b_prefill_production_receipts.json
  ash_attn_headwise_causal_01b_incremental_production_receipts.json
  ash_attn_headwise_causal_01b_chunked_non_promotion_guard.json
  ash_attn_headwise_causal_01b_pipeline_cache_receipt.json
  ash_attn_headwise_causal_01b_performance_catalog.json
  ash_attn_headwise_causal_01b_paired_gpu_timing_receipts.json
  ash_attn_headwise_causal_01b_production_parity_summary.json
  ash_attn_headwise_causal_01b_internal_canary_receipt.json
  ash_attn_headwise_causal_01b_rollback_ledger.json
  ash_attn_headwise_causal_01b_fault_injection_matrix.json
  ash_attn_headwise_causal_01b_negative_control_matrix.json
  ash_attn_headwise_causal_01b_static_checks.json
  ash_attn_headwise_causal_01b_model_quality_claim_guard.json
  ash_attn_headwise_causal_01b_verdict.json
```

Runtime artifacts are excluded from the source bake archive.

---

# 28. Primary artifact ABI

Required flat top-level fields:

```text
schema
patch_id
parent_patch_id
pass
status
verdict
primary_artifact
manifest
parent_01a_artifact_digest
parent_01a_manifest_digest
promotion_policy_digest
model_instance_id
effective_runtime_binding_digest
device_identity_digest
device_epoch
full_prefill_authority_mode
incremental_decode_authority_mode
chunked_decode_authority_mode
admitted_prefill_bucket_count
admitted_incremental_bucket_count
chunked_production_commit_count
same_device_dispatcher
qkv_zero_copy_all
output_zero_copy
output_buffer_identity_match
output_cpu_readback_count
output_host_upload_count
output_tensor_from_data_count
prefill_production_dispatch_count
incremental_production_dispatch_count
atlas_output_commit_count
reference_production_commit_count
mixed_authority_count
future_key_visit_count
bound_mismatch_count
kv_lifecycle_failure_count
pipeline_cache_cold_timed_count
pipeline_creation_timed_count
group_map_upload_timed_count
performance_bucket_count
performance_bucket_fail_count
prefill_geomean_median_ratio
incremental_geomean_median_ratio
worst_bucket_median_ratio
end_to_end_p50_ratio
end_to_end_p95_ratio
rollback_fixture_count
rollback_fixture_fail_count
rollback_reference_retry_count
rollback_kv_double_append_count
silent_fallback_count
negative_control_count
negative_control_fail_count
production_authority_claim_count
model_quality_claim_count
```

---

# 29. PASS formula

```text
PASS =
  parent 01A artifact and manifest bound exactly
  && parent 01A pass=true
  && promotion policy bound to exact model instance
  && dispatcher same-device=true
  && independent adapter/device request count=0
  && Q/K/V zero-copy all=true
  && output zero-copy=true
  && output buffer identity match=true
  && output CPU readback count=0
  && output host upload count=0
  && output Tensor::from_data count=0
  && prefill KV lifecycle matrix pass
  && incremental KV lifecycle matrix pass
  && chunked production commit count=0
  && future key visit count=0
  && bound mismatch count=0
  && parallel group map pass
  && production parity pass
  && finite guard pass
  && timed pipeline creation count=0
  && timed group-map upload count=0
  && every admitted bucket meets performance threshold
  && route-wide promotion threshold met for every route claimed production
  && internal canary pass
  && atlas output commit count>0
  && reference production commit count=0 for admitted atlas routes
  && mixed authority count=0
  && rollback fixture count>0
  && rollback fixture fail count=0
  && rollback KV double-append count=0
  && silent fallback count=0
  && negative control count>=160
  && negative control fail count=0
  && model quality claim count=0
```

PASS proves:

```text
exact full-prefill and incremental-decode buckets may use headwise atlas as production attention-output owner
Q/K/V and output remain on the model's existing WGPU device
attention output is written directly into a GPU-resident native tensor
KV absolute position and append lifecycle are bound to each dispatch
performance does not regress for promoted buckets
reference authority is revoked for those buckets
an explicit single-reference rollback exists before output commit
```

PASS does not prove:

```text
chunked production promotion
all sequence lengths on all GPUs
all model architectures
hardware Tensor Core execution
language-quality improvement
translation-quality improvement
```

---

# 30. Canonical build and run

Expected checks:

```powershell
cargo fmt --all -- --check

cargo check --release --manifest-path crates/burn_webgpu_backend/Cargo.toml

cargo check --release --manifest-path crates/model_core/Cargo.toml

cargo check --release --manifest-path crates/runtime/Cargo.toml

cargo check --release --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01b_gate
```

Canonical run:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01b_gate `
  -- `
  --repo-root . `
  --parent-artifact workspace/runtime/attention/ash_attn_headwise_causal_01a_runtime_artifact.json `
  --parent-manifest workspace/runtime/attention/ash_attn_headwise_causal_01a_local_manifest.json `
  --runtime-profile specs/runtime_profile_v5_48259.toml `
  --promote-full-prefill true `
  --promote-incremental-decode true `
  --promote-chunked-decode false `
  --require-same-device true `
  --require-qkv-zero-copy true `
  --require-output-zero-copy true `
  --forbid-output-readback true `
  --forbid-output-host-upload true `
  --performance-mode paired-gpu-timestamp `
  --warmup-iterations 128 `
  --measurement-pairs 1024 `
  --measurement-rounds 32 `
  --internal-canary-prefills 128 `
  --internal-canary-decode-steps 1024 `
  --fault-injection true `
  --require-rollback true `
  --full-source-hash true `
  --out-dir workspace/runtime/attention
```

Expected PASS token:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_SHADOW_TO_PRODUCTION_AUTHORITY_KV_LIFECYCLE_BOUND_SAME_DEVICE_ZERO_COPY_OUTPUT_PERFORMANCE_NON_REGRESSION_ROLLBACK_SEALED_NO_CHUNKED_PROMOTION_NO_MODEL_QUALITY_OVERCLAIM
```

---

# 31. Promotion boundary after 01B

After 01B PASS:

```text
FullPrefill admitted buckets -> AtlasProduction
IncrementalDecode admitted buckets -> AtlasProduction
non-admitted buckets -> ReferenceProduction
ChunkedDecode -> AtlasShadow / QualifiedCandidate
```

A subsequent patch may address:

```text
ASH-ATTN-HEADWISE-CAUSAL-01C
Chunked Consumer Binding /
Dynamic Sequence-Bucket Router /
Long-Run Production Health /
Cross-Device Performance Catalog Seal
```
