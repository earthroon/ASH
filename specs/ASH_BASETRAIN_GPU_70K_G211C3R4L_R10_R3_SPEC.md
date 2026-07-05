# G211C3R4L-R10-R3
## GPU Readback Output Digest Evidence / MapAsync Real Buffer Hash Seal

## Scope

G211C3R4L-R10-R3 consumes G211C3R4L-R10-R2 as parent evidence. R10-R2 proved digest evidence from canonicalized `MaterializedTensorBytes`, but did not prove mapped GPU readback evidence because `map_async_completed = false` and `readback_buffer_mapped = false`.

R10-R3 requires GPU output digest evidence to come from mapped readback buffer bytes. `MaterializedTensorBytes` may be retained only as a cross-check path and must not be used as the primary GPU digest source.

R10-R3 does not adopt the cache policy as default runtime behavior, does not persist manual opt-in after audit, does not open the runtime splice, and does not declare a performance winner.

## Parent seal

```text
parent_patch_id = G211C3R4L-R10-R2
parent_verdict = PASS_G211C3R4L_R10_R2_LIVE_OUTPUT_BUFFER_DIGEST_EVIDENCE_SEALED
parent_digest_source = MaterializedTensorBytes
parent_limitation = map_async_completed false / readback_buffer_mapped false
```

## Core principle

```text
Primary R10-R3 GPU digest evidence must come from ReadbackBufferBytes.
MaterializedTensorBytes is cross-check only.
No materialized fallback is allowed for the GPU digest PASS path.
```

## GPU readback path

Required path:

```text
storage/output buffer
  -> copy_buffer_to_buffer
  -> readback/staging buffer
  -> queue submit
  -> device poll
  -> map_async
  -> mapped range
  -> digest exact logical output bytes
  -> unmap
```

Required flags:

```text
gpu_output_buffer_present = true
readback_buffer_created = true
copy_to_readback_encoded = true
copy_to_readback_submitted = true
queue_submit_completed = true
device_poll_completed = true
map_async_requested = true
map_async_completed = true
readback_buffer_mapped = true
mapped_range_acquired = true
mapped_range_byte_len = expected_output_byte_len
readback_buffer_unmapped_after_digest = true
```

## Required GPU roles

The following roles require `ReadbackBufferBytes` for R10-R3 PASS:

```text
ManualOptInCandidate
ColdCreateEveryIteration
ParentR9ShadowReplay
ExistingRuntimePrimary
```

Host-only roles may stay materialized:

```text
CpuReference -> MaterializedTensorBytes
BurnBaseline -> MaterializedTensorBytes unless a Burn WebGPU readback path is available
```

## Canonical byte layout

```text
dtype = f32
endianness = little-endian
layout = row-major logical output
shape = [M, N]
element_count = M * N
byte_len = M * N * 4
nan_policy = canonicalize_nan_payloads_before_digest
zero_policy = preserve_signed_zero
padding_policy = no padding bytes included
```

Current fixtures:

```text
M = 16
N = 16
expected_output_byte_len = 1024
```

Readback allocation may be larger, but digest input must be sliced to the exact logical byte length.

## MapAsync contract

PASS requires:

```text
map_async_status = Completed
map_async_requested = true
map_async_completed = true
map_async_failed = false
map_async_timed_out = false
device_poll_completed = true
queue_submit_completed = true
readback_buffer_mapped = true
mapped_range_acquired = true
mapped_range_len_matches_expected = true
readback_buffer_unmapped_after_digest = true
```

## Digest evidence contract

PASS requires:

```text
primary_digest_source = ReadbackBufferBytes
readback_digest_available = true
digest_fields_are_real_sha256 = true
label_fields_used_as_digest = false
fixture_surrogate_used_as_digest = false
materialized_tensor_fallback_used_for_gpu_digest = false
all_digest_fields_are_64_lower_hex = true
digest_input_byte_len = expected_output_byte_len
readback_digest_evidence_passed = true
```

Expected PASS marker:

```text
PASS_G211C3R4L_R10_R3_GPU_READBACK_OUTPUT_DIGEST_EVIDENCE_SEALED
```

Expected fail markers:

```text
FAIL_G211C3R4L_R10_R3_GPU_READBACK_OUTPUT_DIGEST_EVIDENCE
FAIL_G211C3R4L_R10_R3_MATERIALIZED_FALLBACK_NOT_ALLOWED_FOR_GPU_READBACK_SEAL
```

## Readback/materialized cross-check

R10-R3 must compare readback digests with R10-R2 materialized digest evidence.

Required:

```text
manual_readback_matches_materialized_digest = true
cold_readback_matches_materialized_digest = true
parent_r9_readback_matches_materialized_digest = true
primary_readback_matches_materialized_digest = true
materialized_digest_used_as_fallback = false
materialized_digest_used_as_crosscheck_only = true
crosscheck_passed = true
```

## Live tensor comparison preservation

PASS requires:

```text
actual_tensor_compare_used = true
parent_mismatch_counter_replay_used = false
label_compare_used = false
digest_only_compare_used = false
manual_opt_in_cpu_mismatch_count = 0
manual_opt_in_burn_mismatch_count = 0
manual_opt_in_cold_mismatch_count = 0
manual_opt_in_parent_r9_mismatch_count = 0
manual_opt_in_primary_output_mismatch_count = 0
```

## Role separation preservation

```text
selected_default_manual_opt_in_mode = PipelineBuffersBindGroupCachedManualOptIn
FullCandidateResourceCachedManualOptIn in optional_manual_opt_in_modes
full_cache_selected_as_top_level_default = false
OptionalFullCachePass requires --optional-full-cache-opt-in
```

## Timing provenance preservation

R10-R3 does not upgrade synthetic timing to performance evidence.

```text
timing_source_kind = SimulatedFixture for deterministic envelopes
allowed_for_performance_evidence = false
speedup_required_for_pass = false
performance_winner_declared = false
```

## Local artifacts

Generated locally only:

```text
workspace/runtime/tensorcube/g211c3r4l_r10_r3_gpu_readback_capture_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_r3_map_async_evidence_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_r3_readback_digest_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_r3_readback_materialized_crosscheck_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_r3_gpu_readback_digest_evidence_receipt_latest.json
artifacts/g211c3r4l_r10_r3_gpu_readback_digest_evidence_local_manifest.json
```

These files are not committed.

## Audit commands

Conservative GPU readback digest validation:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r10_r3_gpu_readback_digest_evidence_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --manual-opt-in-cache-policy --manual-opt-in-mode pipeline-buffers-bindgroup --require-gpu-readback-digest
```

Optional full-cache GPU readback digest validation:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r10_r3_gpu_readback_digest_evidence_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --manual-opt-in-cache-policy --manual-opt-in-mode pipeline-buffers-bindgroup --optional-full-cache-opt-in --require-gpu-readback-digest
```

Strict full evidence validation:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r10_r3_gpu_readback_digest_evidence_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --manual-opt-in-cache-policy --manual-opt-in-mode pipeline-buffers-bindgroup --optional-full-cache-opt-in --require-gpu-readback-digest --require-map-async --require-live-tensor-compare --require-parent-r9-shadow-replay-readback
```

Blocked fallback validation:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r10_r3_gpu_readback_digest_evidence_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --manual-opt-in-cache-policy --manual-opt-in-mode pipeline-buffers-bindgroup --require-gpu-readback-digest --allow-materialized-fallback
```

## PASS conditions

```text
parent_patch_id = G211C3R4L-R10-R2
parent_verdict = PASS_G211C3R4L_R10_R2_LIVE_OUTPUT_BUFFER_DIGEST_EVIDENCE_SEALED
role_separation_passed = true
gpu_readback_bytes_captured = true
map_async_completed = true
readback_buffer_mapped = true
readback_digest_available = true
readback_digest_evidence_passed = true
primary_digest_source = ReadbackBufferBytes
materialized_tensor_fallback_used_for_gpu_digest = false
fixture_surrogate_used_as_digest = false
label_fields_used_as_digest = false
readback_materialized_crosscheck_passed = true
digest_comparison_passed = true
live_tensor_comparison_passed = true
comparison_provenance_passed = true
parent_r9_shadow_replay_executed = true
parent_r9_shadow_replay_readback_mapped = true
parent_r9_shadow_replay_digest_passed = true
correctness_gate_passed = true
timestamp_gate_passed = true
guard_gate_passed = true
ownership_gate_passed = true
rollback_gate_passed = true
default_policy_disabled = true
default_runtime_policy_adopted = false
automatic_promotion_allowed = false
manual_opt_in_persisted_after_run = false
performance_winner_declared = false
hardware_tensorcore_claimed = false
failures = []
```

## Failure conditions

```text
FAIL: GPU output buffer unavailable
FAIL: readback buffer not created
FAIL: copy_to_readback not encoded
FAIL: queue submit not completed
FAIL: device poll not completed
FAIL: map_async not requested
FAIL: map_async not completed
FAIL: map_async failed
FAIL: map_async timed out
FAIL: readback buffer not mapped
FAIL: mapped range not acquired
FAIL: mapped range byte length mismatch
FAIL: readback buffer not unmapped after digest
FAIL: primary_digest_source != ReadbackBufferBytes
FAIL: digest_source = MaterializedTensorBytes for GPU digest PASS path
FAIL: materialized tensor fallback used for GPU digest
FAIL: digest_source = FixtureSurrogateBytes
FAIL: digest_source = DebugLabelBytes
FAIL: fixture_surrogate_used_as_digest = true
FAIL: label_fields_used_as_digest = true
FAIL: parent R9 shadow replay readback unavailable
FAIL: parent R9 shadow replay used previous receipt label
FAIL: parent R9 shadow replay used previous digest without replay
FAIL: readback/materialized crosscheck failed
FAIL: digest-only comparison used as tensor correctness
FAIL: actual tensor compare not used
FAIL: parent mismatch counter replay used while live comparison is claimed
FAIL: full-cache mode selected as top-level default
FAIL: optional full-cache pass without explicit flag
FAIL: manual_opt_in_persisted_after_run = true
FAIL: performance_winner_declared = true
FAIL: hardware_tensorcore_claimed = true
```

## Final seal

R10-R3 is accepted only if GPU digest evidence is derived from mapped ReadbackBufferBytes, map_async is completed and recorded, MaterializedTensorBytes remains cross-check only, parent R9 shadow output is replayed and read back under the current input SSOT, and no timing/performance/runtime-adoption claim is silently upgraded.
