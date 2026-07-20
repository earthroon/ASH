# ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R2-R1-R2-R1
# Live Fusion Last-Logits Resolution / External Fixture Override Map Semantic Separation / GPU-Only Fusion Client Resolve / Same-Device Raw Resource Borrow / Stage-Exact Policy Binding and Terminal Receipt / Non-Vacuous Authority Reducer Repair Seal

- Patch ID: `ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R2-R1-R2-R1_LIVE_FUSION_LAST_LOGITS_RESOLUTION_EXTERNAL_FIXTURE_OVERRIDE_MAP_SEMANTIC_SEPARATION_GPU_ONLY_FUSION_CLIENT_RESOLVE_SAME_DEVICE_RAW_RESOURCE_BORROW_STAGE_EXACT_POLICY_BINDING_AND_TERMINAL_RECEIPT_NON_VACUOUS_AUTHORITY_REDUCER_REPAIR_SEAL`
- Parent: `ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R2-R1-R2`
- Strict GPU policy: `strict_same_device_gpu_last_logits_v2`
- Live resolution policy: `strict_live_fusion_same_device_raw_resolve_v1`
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R5-R1-R8-R2-R2-R1-R2-R2`
- R8-R2-R3 authorization: `false`
- R8-R3 authorization: `false`
- R4-R5-R2 authorization: `false`
- Legacy oracle removal: `false`
- Legacy decoder retirement: `false`
- General production apply: `false`

## 1. Parent failure

The parent strict GPU-only run admitted all 16 workers and kept CPU materialization, host upload, legacy GPU fallback, and CPU oracle counters at zero. Greedy and sampled workers stopped before the first authoritative token with the same error:

```text
strict_gpu_same_device_raw_bridge_failed
reason=PrimitiveHandleMapMiss
raw_borrows=0
host_uploads=0
handle_hits=0
handle_misses=1
```

The same workers reported:

```text
registry_register_ok=true
runtime_handles_ok=true
raw_bridge_ok=true
gpu_sampling_ok=true
gpu_penalty_ok=true
```

`PrimitiveHandleMapMiss` therefore does not prove that the live GPU buffer or runtime handles are absent. It proves that the live Fusion tensor was queried through an external fixture override registry that did not own it.

## 2. Canonical ownership

A live Fusion tensor is owned by the Fusion client that created and tracks it.

```text
live Fusion last-logits
→ owning Fusion client
→ resolve_tensor_float on GPU
→ resolved CubeTensor
→ CubeTensor client raw-resource borrow
→ same-device RawWgpuBufferLease
→ strict GPU argmax or strict GPU sampler
```

Forbidden:

```text
live Fusion last-logits
→ external fixture override map
→ PrimitiveHandleMap lookup
```

The external override map remains valid only for explicitly registered fixtures and external aliases.

## 3. Live GPU-only resolution

The canonical resolver is equivalent to:

```rust
let fusion_tensor = extract_fusion_tensor(tensor)?;
let client = fusion_tensor.client.clone();
let resolved = client.resolve_tensor_float::<NativeWgpuRawBackend>(
    fusion_tensor.clone(),
);
```

Required path:

```text
fusion_client.resolve_tensor_float_gpu_only
```

The live resolver MUST NOT call:

```text
try_resolve_external_float_primitive_for_fusion_tensor
register_native_wgpu_fixture_primitive_for_fusion_tensor
Tensor::into_data
Tensor::to_data
Tensor::into_scalar
```

Required result semantics:

```text
host_materialization_performed=false
host_upload_performed=false
external_fixture_map_used=false
```

## 4. Same-device raw resource borrow

The resolved `CubeTensor<WgpuRuntime>` is borrowed only through:

```text
try_borrow_cube_tensor_raw_resource
```

Required identity equality:

```text
model device
= generation device
= resolved primitive device
= raw resource device
= selector device
```

Required queue equality:

```text
generation queue
= raw resource queue
= selector queue
```

The lease references the original resource. Reconstructing a GPU buffer from host bytes is forbidden.

## 5. Strict bridge

Required strict API:

```text
bridge_native_tensor_f32_live_outcome_strict
```

Required flow:

```text
validate strict policy
→ resolve through owning Fusion client
→ borrow original raw resource
→ return SameDeviceBorrow
```

Forbidden in the strict live call graph:

```text
bridge_native_tensor_f32_or_fail
bridge_native_tensor_f32_or_fallback
upload_tensor_f32
external fixture registry lookup
CPU materialization
legacy selector fallback
```

Resolution or raw-borrow failure returns HOLD with zero contribution and never descends to another selector in the same worker.

## 6. Fixture semantic firewall

The live resolver does not inspect the fixture registry even to test whether an override exists.

If the strict live path enters the fixture registry:

```text
outcome=FAIL
error_class=StrictLivePathEnteredExternalFixtureRegistry
authoritative contribution=0
```

Fixture probes remain available through explicitly fixture-scoped APIs and receipts.

## 7. Bridge telemetry

Required counters:

```text
live_fusion_resolve_attempts
live_fusion_resolve_hits
live_fusion_resolve_failures
live_raw_resource_borrow_attempts
live_raw_resource_borrow_hits
live_raw_resource_borrow_failures
external_fixture_map_attempts
external_fixture_map_hits
external_fixture_map_misses
raw_borrows
host_uploads
```

Strict live PASS requires:

```text
live_fusion_resolve_attempts > 0
live_fusion_resolve_hits = live_fusion_resolve_attempts
live_fusion_resolve_failures = 0
live_raw_resource_borrow_attempts > 0
live_raw_resource_borrow_hits = live_raw_resource_borrow_attempts
live_raw_resource_borrow_failures = 0
external_fixture_map_attempts = 0
external_fixture_map_hits = 0
external_fixture_map_misses = 0
host_uploads = 0
```

## 8. Stage-exact evidence

`worker_summary.json` is not policy-binding authority because it is written only after all generations finish.

Each admitted worker emits Rust-owned stage evidence:

```text
worker_model_load.json
worker_model_policy_binding.json
worker_runtime_handles.json
worker_generation_start.json
worker_terminal_outcome.json
```

`worker_model_policy_binding.json` is written after model policy binding and before generation. It records:

```text
strict_policy_object_present
canonical_policy_validation_pass
policy_id
policy_digest
runtime_handles_ready
gpu_sampling_runtime_ready
gpu_penalty_runtime_ready
live_fusion_resolver_ready
binding_completed_before_generation
pass
```

`policy_binding_pass` is reduced from these receipts and is not inferred from worker-summary presence.

## 9. Mandatory terminal outcome

Every admitted worker emits `worker_terminal_outcome.json` for Success, HOLD, or FAIL.

Terminal stages include:

```text
ModelLoading
ModelLoaded
PolicyBinding
PolicyBound
RuntimeHandlesValidated
GenerationStarted
LastLogitsProduced
LiveFusionResolving
LiveFusionResolved
RawResourceBorrowing
RawResourceBorrowed
GreedyDispatching
SampledDispatching
SelectionReadback
ReceiptConstructing
TokenCommitting
WorkerCompleted
```

Terminal error classes include:

```text
None
ModelLoadFailed
PolicyObjectMissing
PolicyDigestMismatch
RuntimeHandlesUnavailable
LiveFusionTensorExtractionFailed
LiveFusionClientResolutionFailed
LiveFusionResolvedPrimitiveUnavailable
SameDeviceRawResourceBorrowFailed
DeviceIdentityMismatch
QueueIdentityMismatch
StrictLivePathEnteredExternalFixtureRegistry
NativeGpuArgmaxDispatchFailed
StrictGpuSamplerDispatchFailed
CompactReadbackFailed
CpuMaterializeAttempted
HostUploadAttempted
LegacyGpuFallbackAttempted
CpuOracleAttempted
ReceiptIntegrityFailure
ChildExitWithoutWorkerReceipt
Unknown
```

The coordinator publishes terminal-stage and terminal-error-class histograms.

## 10. HOLD and FAIL

HOLD with zero contribution:

```text
live Fusion resolution unavailable
raw resource borrow unavailable
native GPU argmax dispatch failure before commit
strict GPU sampler dispatch failure before commit
compact readback failure before commit
device loss before commit
```

FAIL with zero contribution:

```text
strict live path enters fixture registry
CPU materialization attempt
host upload attempt
legacy GPU fallback attempt
CPU oracle attempt
policy, device, queue, or lease identity mismatch
non-authoritative or partial token commit
```

## 11. Non-vacuous reducer

The equality below is insufficient when both values are zero:

```text
authoritative_selected_token_count
= same_device_raw_selected_token_count
```

Required same-device PASS:

```text
authoritative_selected_token_count > 0
AND authoritative_selected_token_count = same_device_raw_selected_token_count
AND live_fusion_resolve_hits > 0
AND live_raw_resource_borrow_hits > 0
AND all identity mismatch counters = 0
AND external_fixture_map_attempts = 0
```

Required authority PASS:

```text
greedy authoritative selected tokens > 0
sampled authoritative selected tokens > 0
native GPU argmax count = greedy selected tokens
strict GPU sampler count = sampled selected tokens
```

Required evidence integrity:

```text
worker policy-binding receipts = worker processes
worker terminal receipts = worker processes
child exits without terminal receipt = 0
unknown terminal errors = 0
authoritative selected tokens > 0
missing token receipts = 0
duplicate token receipts = 0
non-authoritative commits = 0
receipt digest mismatches = 0
```

## 12. Static call-graph seal

Required symbols:

```text
resolve_live_native_wgpu_float_primitive
fusion client resolve_tensor_float
try_borrow_cube_tensor_raw_resource
bridge_native_tensor_f32_live_outcome_strict
strict_gpu_greedy_choice
strict_gpu_sampled_choice
```

Forbidden symbols in the strict live graph:

```text
try_resolve_external_float_primitive_for_fusion_tensor
register_native_wgpu_fixture_primitive_for_fusion_tensor
bridge_native_tensor_f32_or_fail
bridge_native_tensor_f32_or_fallback
upload_tensor_f32
Tensor::into_data
Tensor::to_data
Tensor::into_scalar
dispatch_sample_raw_lease_legacy
select_next_token_with_cpu_oracle
```

## 13. Worker matrix and smoke

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

Each route completes at least 100 generations and 2500 authoritative selected tokens.

## 14. Rust-owned artifacts

All runtime evidence is emitted by Rust. Scripts are not promotion authority.

```text
workspace/runtime/tensorcube/
ash_tensorcube_decode_04_r4_r5_r1_r8_r2_r2_r1_r2_r1_runtime_artifact.json

workspace/runtime/tensorcube/
ash_tensorcube_decode_04_r4_r5_r1_r8_r2_r2_r1_r2_r1_local_manifest_latest.json

workspace/runtime/tensorcube/soak/
r4_r5_r1_r8_r2_r2_r1_r2_r1/workers/<worker_id>/

workspace/runtime/tensorcube/soak/
r4_r5_r1_r8_r2_r2_r1_r2_r1/live_fusion_resolution_static_audit.json

workspace/runtime/tensorcube/soak/
r4_r5_r1_r8_r2_r2_r1_r2_r1/worker_terminal_stage_histogram.json
```

## 15. PASS authority

PASS requires:

```text
strict_worker_admission_count=16
worker_process_count=16
worker_policy_binding_receipt_count=16
worker_terminal_receipt_count=16
worker_success_count=16
worker_hold_count=0
worker_fail_count=0
live_fusion_resolve_failure_count=0
live_raw_resource_borrow_failure_count=0
external_fixture_map_attempt_count=0
all forbidden counters=0
all truth checks=true
```

PASS sets only:

```text
r4_r5_r1_r8_r2_r2_r1_r2_r1_live_fusion_resolution_pass=true
r4_r5_r1_r8_r2_r2_r1_r2_r2_authorized=true
```

Still false:

```text
r4_r5_r1_r8_r2_r3_authorized=false
r4_r5_r1_r8_r3_authorized=false
decode04_r4_r5_r2_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
general_production_apply_authorized=false
```

## 16. Verdict markers

```text
PASS_ASH_TCU_DECODE_04_R4_R5_R1_R8_R2_R2_R1_R2_R1_LIVE_FUSION_LAST_LOGITS_RESOLUTION_SEAL
HOLD_ASH_TCU_DECODE_04_R4_R5_R1_R8_R2_R2_R1_R2_R1_LIVE_FUSION_LAST_LOGITS_RESOLUTION_SEAL
FAIL_ASH_TCU_DECODE_04_R4_R5_R1_R8_R2_R2_R1_R2_R1_LIVE_FUSION_RESOLUTION_INVARIANT_VIOLATION
```

## 17. Canonical seal

```text
A live Fusion tensor is resolved by the Fusion client that owns it.
The strict path borrows the original same-device raw resource and does
not inspect fixture overrides, materialize logits on CPU, upload host
bytes, or descend into legacy selection.

Policy binding, live resolution, raw borrowing, selection, and terminal
outcome are separate evidence stages. No zero-token execution passes an
authority, same-device, receipt, or evidence-integrity check merely
because two empty counters are equal.
```
