# G211C3R4L-R10-R2
## Live Output Buffer Digest Evidence Attach / Manual Opt-In Real Output Hash Seal

## Scope

G211C3R4L-R10-R2 consumes G211C3R4L-R10-R1 as parent evidence. R10-R1 fixed optional full-cache role classification and timing provenance, but strict digest validation failed because the digest source was `FixtureSurrogateBytes` and `real_output_buffer_digest_available = false`.

R10-R2 attaches real materialized output bytes to the digest path. Debug labels, fixture IDs, input hashes, and receipt strings remain metadata only and cannot be used as digest evidence.

R10-R2 does not adopt the cache policy as default runtime behavior, does not persist manual opt-in after audit, does not open the runtime splice, and does not declare a performance winner.

## Parent seal

```text
parent_patch_id = G211C3R4L-R10-R1
parent_role_separation_status = PASS
parent_timing_provenance_status = PASS
parent_strict_digest_status = FAIL_G211C3R4L_R10_R1_OUTPUT_DIGEST_NOT_REAL
parent_failure = real output buffer digest unavailable
```

## Core principle

```text
Digest fields must be derived from actual materialized output bytes.
Debug labels are labels.
Fixture surrogate bytes are forbidden as digest evidence.
```

## Output byte sources

Required output roles:

```text
ExistingRuntimePrimary
ColdCreateEveryIteration
ManualOptInCandidate
ParentR9ShadowReplay
BurnBaseline
CpuReference
```

Allowed byte sources for R10-R2 PASS:

```text
ReadbackBufferBytes
MaterializedTensorBytes
ParentR9ShadowReplayBytes
```

Forbidden byte sources:

```text
FixtureSurrogateBytes
DebugLabelBytes
InputHashBytes
ReceiptStringBytes
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

For the current fixtures:

```text
M = 16
N = 16
expected_output_byte_len = 1024
```

## Digest evidence contract

PASS requires:

```text
live_output_bytes_captured = true
real_output_buffer_digest_available = true
output_digest_evidence_passed = true
output_digest_source = OutputBufferBytes or MaterializedTensorBytes or ParentR9ShadowReplayBytes
fixture_surrogate_used_as_digest = false
label_fields_used_as_digest = false
all_digest_fields_are_64_lower_hex = true
digest_input_byte_len = expected_output_byte_len
```

Expected PASS marker:

```text
PASS_G211C3R4L_R10_R2_LIVE_OUTPUT_BUFFER_DIGEST_EVIDENCE_SEALED
```

Expected FAIL marker:

```text
FAIL_G211C3R4L_R10_R2_REAL_OUTPUT_DIGEST_EVIDENCE
```

## Digest comparison contract

Digest equality is evidence that captured byte streams match exactly. It is not a substitute for tensor correctness unless live tensor comparison provenance also passes.

Required comparisons:

```text
manual_opt_in_digest == cpu_reference_digest
manual_opt_in_digest == burn_baseline_digest
manual_opt_in_digest == cold_output_digest
manual_opt_in_digest == parent_r9_shadow_replay_digest
manual_opt_in_digest == existing_runtime_primary_digest
```

Required:

```text
digest_comparison_passed = true
digest_only_compare_used_as_correctness = false
```

## Live tensor comparison provenance

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

R10-R2 does not upgrade timing evidence. Synthetic timing remains `SimulatedFixture` and cannot be used as performance evidence.

```text
speedup_required_for_pass = false
performance_winner_declared = false
```

## Local artifacts

Generated locally only:

```text
workspace/runtime/tensorcube/g211c3r4l_r10_r2_live_output_capture_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_r2_real_output_digest_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_r2_digest_comparison_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_r2_live_comparison_provenance_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_r2_live_output_digest_evidence_receipt_latest.json
artifacts/g211c3r4l_r10_r2_live_output_digest_evidence_local_manifest.json
```

These files are not committed.

## Audit commands

Conservative real digest validation:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r10_r2_live_output_digest_evidence_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --manual-opt-in-cache-policy --manual-opt-in-mode pipeline-buffers-bindgroup --require-real-output-digest
```

Optional full-cache real digest validation:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r10_r2_live_output_digest_evidence_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --manual-opt-in-cache-policy --manual-opt-in-mode pipeline-buffers-bindgroup --optional-full-cache-opt-in --require-real-output-digest
```

Strict full evidence validation:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r10_r2_live_output_digest_evidence_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --manual-opt-in-cache-policy --manual-opt-in-mode pipeline-buffers-bindgroup --optional-full-cache-opt-in --require-real-output-digest --require-live-tensor-compare --require-parent-r9-shadow-replay
```

## PASS conditions

```text
parent_patch_id = G211C3R4L-R10-R1
role_separation_passed = true
live_output_bytes_captured = true
real_output_buffer_digest_available = true
output_digest_evidence_passed = true
fixture_surrogate_used_as_digest = false
label_fields_used_as_digest = false
digest_comparison_passed = true
live_tensor_comparison_passed = true
comparison_provenance_passed = true
parent_r9_shadow_replay_executed = true
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
FAIL: live output bytes unavailable
FAIL: digest_source = FixtureSurrogateBytes
FAIL: digest_source = DebugLabelBytes
FAIL: fixture_surrogate_used_as_digest = true
FAIL: label_fields_used_as_digest = true
FAIL: real_output_buffer_digest_available = false
FAIL: digest_input_byte_len != expected_output_byte_len
FAIL: parent R9 shadow replay output bytes unavailable
FAIL: digest comparison failed
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

R10-R2 is accepted only if digest fields are computed from materialized output bytes, role separation remains intact, parent R9 shadow output is replayed as bytes under the current input SSOT, and no timing/performance/runtime-adoption claim is silently upgraded.
