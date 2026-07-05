# G211C3R4L-R10-R1
## Optional Full-Cache Opt-In Role Separation / Evidence Provenance Hotfix Seal

## Scope

G211C3R4L-R10-R1 consumes the failed G211C3R4L-R10 receipt as parent evidence. R10 failed because optional full-cache manual opt-in fixtures were classified as default mode adoption. R10-R1 separates top-level default manual opt-in mode from fixture-local active mode and optional pass role.

R10-R1 also hardens evidence provenance. Synthetic timing envelopes must not be labeled as measured HostInstant or GpuTimestampQuery data. Output labels must not be used as output digests. If real output buffer bytes are unavailable, the receipt must say so and strict real-output-digest validation must fail rather than silently passing.

R10-R1 does not adopt the cache policy as default runtime behavior, does not persist manual opt-in after audit, does not open the runtime splice, and does not declare a performance winner.

## Parent failure seal

```text
parent_patch_id = G211C3R4L-R10
parent_verdict = FAIL_G211C3R4L_R10_LIMITED_SHADOW_ENABLE_GATE
observed_failure = full-cache opt-in selected as default
```

R10 preserved important safety lines:

```text
manual_opt_in_requested = true
default_policy_disabled = true
default_runtime_policy_adopted = false
automatic_promotion_allowed = false
manual_opt_in_persisted_after_run = false
performance_winner_declared = false
hardware_tensorcore_claimed = false
```

## Core principle

```text
Fix the role classification bug.
Do not erase the parent FAIL.
Do not turn evidence labels into proof.
```

## Role separation model

R10-R1 separates:

```text
top_level_default_manual_opt_in_mode
fixture_active_manual_opt_in_mode
fixture_role
optional_full_cache_opt_in_requested
optional_manual_opt_in_modes
```

Allowed optional full-cache pass:

```text
top_level_default_manual_opt_in_mode = PipelineBuffersBindGroupCachedManualOptIn
fixture_active_manual_opt_in_mode = FullCandidateResourceCachedManualOptIn
fixture_role = OptionalFullCachePass
optional_full_cache_opt_in_requested = true
FullCandidateResourceCachedManualOptIn in optional_manual_opt_in_modes
```

Hard failure only when:

```text
top_level_default_manual_opt_in_mode = FullCandidateResourceCachedManualOptIn
```

## Timing provenance contract

R10 timing samples showed deterministic repeated envelopes such as `x, x+0.25, x+0.5` repeated. These samples must not be labeled as measured HostInstant or measured GpuTimestampQuery evidence.

Timing source kinds:

```text
MeasuredHostInstant
MeasuredGpuTimestampQuery
SimulatedFixture
DerivedEnvelope
```

Timing evidence roles:

```text
PerformanceEvidence
DiagnosticOnly
StructuralFixtureOnly
```

Rules:

```text
FAIL if synthetic timing pattern is labeled HostInstant
FAIL if synthetic timing pattern is labeled GpuTimestampQuery
PASS if synthetic fixture timing is labeled SimulatedFixture and StructuralFixtureOnly
PASS if derived timing envelope is labeled DerivedEnvelope and DiagnosticOnly
```

Expected failure marker for mislabeling:

```text
FAIL_G211C3R4L_R10_R1_TIMING_PROVENANCE_MISLABELED
```

## Output digest contract

R10 output_hash values were debug labels, not digest evidence. R10-R1 separates labels and digests.

```text
*_output_label = human/debug label
*_output_digest_sha256 = 64 lowercase hex digest
```

Strict real digest PASS requires:

```text
digest_source = OutputBufferBytes
digest_input_byte_len > 0
digest_fields_are_real_sha256 = true
label_fields_used_as_digest = false
```

If only fixture surrogate bytes are available, the receipt may create a 64-hex diagnostic digest, but it must use:

```text
digest_source = FixtureSurrogateBytes
real_output_buffer_digest_available = false
output_digest_evidence_passed = false when --require-real-output-digest is supplied
```

This prevents debug labels from masquerading as output-buffer evidence.

Expected failure marker for real digest absence:

```text
FAIL_G211C3R4L_R10_R1_OUTPUT_DIGEST_NOT_REAL
```

## Comparison provenance contract

Mismatch counts may only be trusted if comparison provenance states that actual tensor comparison was used.

Required:

```text
actual_tensor_compare_used = true
label_compare_used = false
digest_only_compare_used = false
```

If R10-R1 only replays parent mismatch counters without direct tensor comparison, it must mark this as derived parent evidence and avoid claiming a new live tensor comparison.

## Local artifacts

Generated locally only:

```text
workspace/runtime/tensorcube/g211c3r4l_r10_r1_role_separation_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_r1_timing_provenance_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_r1_output_digest_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_r1_comparison_provenance_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_r1_hotfix_receipt_latest.json
artifacts/g211c3r4l_r10_r1_opt_in_role_separation_hotfix_local_manifest.json
```

These files are not committed.

## Audit commands

Role separation hotfix validation:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r10_r1_opt_in_role_separation_hotfix_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --manual-opt-in-cache-policy --manual-opt-in-mode pipeline-buffers-bindgroup --optional-full-cache-opt-in
```

Timing provenance validation:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r10_r1_opt_in_role_separation_hotfix_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --manual-opt-in-cache-policy --manual-opt-in-mode pipeline-buffers-bindgroup --optional-full-cache-opt-in --require-timing-provenance
```

Strict real output digest validation:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r10_r1_opt_in_role_separation_hotfix_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --manual-opt-in-cache-policy --manual-opt-in-mode pipeline-buffers-bindgroup --optional-full-cache-opt-in --require-real-output-digest
```

## PASS verdicts

Role separation and provenance labeling pass:

```text
PASS_G211C3R4L_R10_R1_OPT_IN_ROLE_SEPARATION_HOTFIX_SEALED
```

Strict real digest must only pass when output buffer bytes are actually digested.

```text
PASS_G211C3R4L_R10_R1_REAL_OUTPUT_DIGEST_EVIDENCE_SEALED
```

## PASS conditions

```text
parent_patch_id = G211C3R4L-R10
parent_verdict = FAIL_G211C3R4L_R10_LIMITED_SHADOW_ENABLE_GATE
selected_default_manual_opt_in_mode = PipelineBuffersBindGroupCachedManualOptIn
FullCandidateResourceCachedManualOptIn in optional_manual_opt_in_modes
role_separation_passed = true
optional_full_cache_classification_passed = true
timing_provenance_passed = true
timing_samples_mislabeled_as_measured = false
output_hash_labels_renamed = true
comparison_provenance_recorded = true
default_policy_disabled = true
default_runtime_policy_adopted = false
automatic_promotion_allowed = false
manual_opt_in_persisted_after_run = false
rollback_restores_disabled_state = true
speedup_required_for_pass = false
performance_winner_declared = false
runtime_inference_replacement_allowed = false
backend_policy_connection_allowed = false
hardware_tensorcore_claimed = false
```

## Failure conditions

```text
FAIL: top_level_default_manual_opt_in_mode = FullCandidateResourceCachedManualOptIn
FAIL: fixture active full-cache mode classified as default mode
FAIL: fixture_role = OptionalFullCachePass but optional_full_cache_opt_in_requested = false
FAIL: synthetic timing pattern labeled as HostInstant
FAIL: synthetic timing pattern labeled as GpuTimestampQuery
FAIL: timing_source_kind = SimulatedFixture but timer_source_label != SimulatedFixture
FAIL: output digest field contains label prefix
FAIL: output digest field is not 64 lowercase hex
FAIL: label_fields_used_as_digest = true
FAIL: --require-real-output-digest supplied while digest_source != OutputBufferBytes
FAIL: actual_tensor_compare_used = false while live comparison is claimed
FAIL: default_runtime_policy_adopted = true
FAIL: automatic_promotion_allowed = true
FAIL: manual_opt_in_persisted_after_run = true
FAIL: rollback_restores_disabled_state = false
FAIL: performance_winner_declared = true
FAIL: hardware_tensorcore_claimed = true
```

## Final seal

R10-R1 is accepted only if optional full-cache mode is treated as an optional pass, not a default-mode adoption, and if timing/output evidence provenance is explicit enough that downstream gates cannot mistake synthetic labels for measured proof.
