# G211C3R4L-R5
## GPU Timestamp Phase Probe / Command Encoder Marker Timing Seal

## Scope

G211C3R4L-R5 adds candidate-side GPU timestamp query observation on top of the G211C3R4L-R4 timing phase split seal. It keeps the Burn WebGPU matmul baseline and the QW-55A-0-R3 Logical16 KPanel candidate aligned through the same input SSOT and preserves R4 correctness gates.

R5 does not declare a performance winner. It records candidate command encoder timestamp markers and keeps host-boundary timing separate from GPU timestamp timing.

## Parent seal

```text
parent_patch_id = G211C3R4L-R4
parent_verdict = PASS_G211C3R4L_R4_BENCHMARK_TIMING_PHASE_SPLIT_SEALED
baseline_target_kind = BurnWebGpuMatmul
candidate_target_kind = Logical16FromTile8SoftGroupKPanel
```

## Timestamp feature contract

Strict R5 PASS requires:

```text
timestamp_query_supported = true
timestamp_inside_encoder_supported = true
strict_timestamp_pass = true
candidate_gpu_timer_source = GpuTimestampQuery
```

Blocked verdicts:

```text
BLOCKED_G211C3R4L_R5_TIMESTAMP_QUERY_UNAVAILABLE
BLOCKED_G211C3R4L_R5_TIMESTAMP_INSIDE_ENCODER_UNAVAILABLE
BLOCKED_G211C3R4L_R5_PARENT_R4_RECEIPT_UNAVAILABLE
```

## Device request contract

```text
required_limits = adapter.limits()
required_features includes TIMESTAMP_QUERY
required_features includes TIMESTAMP_QUERY_INSIDE_ENCODERS
required_features includes TIMESTAMP_QUERY_INSIDE_PASSES if supported
```

Forbidden:

```text
required_features = empty while creating timestamp query set
downlevel_defaults lowering storage-buffer limits
candidate fifth storage binding
```

## Candidate storage layout

Candidate path must keep the QW-55A-0-R3 four-storage-buffer control_words layout.

```text
binding(0): A atlas
binding(1): B atlas
binding(2): C atlas
binding(3): control_words
```

Timestamp query resources are not shader storage bindings.

```text
timestamp_query_set != storage buffer
timestamp_resolve_buffer != candidate shader storage binding
timestamp_readback_buffer != candidate shader storage binding
```

## Required command encoder markers

```text
candidate_encoder_begin
candidate_before_compute_pass
candidate_before_dispatch
candidate_after_dispatch
candidate_after_compute_pass
candidate_before_copy_to_readback
candidate_after_copy_to_readback
candidate_before_timestamp_resolve
candidate_after_timestamp_resolve
candidate_encoder_finish
```

Strict PASS requires:

```text
missing_timestamp_markers = []
timestamp_marker_coverage_ratio = 1.0
timestamp_query_created = true
timestamp_query_resolved = true
timestamp_readback_mapped = true
timestamp_period_ns_present = true
timestamp_ticks_resolved = true
timestamp_us_converted = true
```

## Required phase stats

GPU timestamp phases:

```text
gpu_candidate_dispatch_body_us
gpu_candidate_compute_pass_us
gpu_candidate_copy_to_readback_us
gpu_candidate_timestamp_resolve_us
gpu_candidate_encoder_total_us
```

Host boundary phases:

```text
host_candidate_total_us
host_candidate_queue_submit_us
host_candidate_poll_map_wait_us
```

Burn timing may remain host-boundary only:

```text
burn_timer_source = HostInstantFromBurnMatmulBoundary
```

## Measurement policy

```text
warmup_iterations >= 5
measure_iterations >= 30
outlier_policy = trim_min_max_one_each_if_samples_ge_10
```

Raw samples must remain in the receipt.

## Correctness preservation

R5 preserves the parent correctness gates:

```text
Burn vs CPU reference
Candidate vs CPU reference
Candidate vs Burn
```

Required:

```text
burn_cpu_mismatch_count = 0
candidate_cpu_mismatch_count = 0
candidate_burn_mismatch_count = 0
burn_nan_count = 0
candidate_nan_count = 0
burn_inf_count = 0
candidate_inf_count = 0
```

## Runtime mutation seal

```text
runtime_inference_replacement_allowed = false
sft_pass1_replacement_allowed = false
backend_policy_connection_allowed = false
subgroup_fast_path_enabled = false
cooperative_matrix_claimed = false
hardware_tensorcore_claimed = false
speedup_required_for_pass = false
performance_winner_declared = false
```

## Local artifacts

Generated locally only:

```text
workspace/runtime/tensorcube/g211c3r4l_r5_gpu_timestamp_fixture_latest.json
workspace/runtime/tensorcube/g211c3r4l_r5_gpu_timestamp_markers_latest.json
workspace/runtime/tensorcube/g211c3r4l_r5_candidate_gpu_phase_timing_latest.json
workspace/runtime/tensorcube/g211c3r4l_r5_host_phase_timing_latest.json
workspace/runtime/tensorcube/g211c3r4l_r5_gpu_timestamp_phase_probe_receipt_latest.json
artifacts/g211c3r4l_r5_gpu_timestamp_phase_probe_local_manifest.json
```

These files are not committed.

## Audit commands

Default:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r5_gpu_timestamp_phase_probe_audit
```

Strict:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r5_gpu_timestamp_phase_probe_audit -- --require-native-adapter
```

With fixtures and timing options:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r5_gpu_timestamp_phase_probe_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30
```

## PASS verdict

```text
PASS_G211C3R4L_R5_GPU_TIMESTAMP_PHASE_PROBE_SEALED
```

PASS means candidate command encoder timestamp markers were created, resolved, mapped, converted, and recorded while parent correctness remained intact. PASS does not mean the Logical16 candidate is faster than Burn.

## Failure conditions

```text
FAIL: parent_patch_id != G211C3R4L-R4
FAIL: parent R4 verdict is not PASS
FAIL: baseline_target_kind != BurnWebGpuMatmul
FAIL: candidate_target_kind != Logical16FromTile8SoftGroupKPanel
FAIL: same_input_ssot_used = false
FAIL: cpu_reference_used_as_benchmark_baseline = true
FAIL: timestamp query set creation failed when feature is supported
FAIL: timestamp resolve buffer missing
FAIL: timestamp readback map failed
FAIL: timestamp_period_ns_present = false
FAIL: timestamp_ticks_resolved = false
FAIL: timestamp_us_converted = false
FAIL: missing_timestamp_markers not empty in strict mode
FAIL: timestamp_marker_coverage_ratio < 1.0 in strict mode
FAIL: gpu_candidate_phase_stats empty
FAIL: timestamp_phase_stats_computed = false
FAIL: timestamp_phase_sum_check_passed = false
FAIL: burn correctness mismatch > 0
FAIL: candidate correctness mismatch > 0
FAIL: candidate vs Burn mismatch > 0
FAIL: performance_winner_declared = true
FAIL: runtime_inference_replacement_allowed = true
FAIL: backend_policy_connection_allowed = true
FAIL: hardware_tensorcore_claimed = true
FAIL: candidate uses fifth storage binding
```
