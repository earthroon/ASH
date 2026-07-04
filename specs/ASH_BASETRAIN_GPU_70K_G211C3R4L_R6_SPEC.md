# G211C3R4L-R6
## Candidate Resource Reuse Probe / Pipeline-BindGroup-Buffer Cache Timing Seal

## Scope

G211C3R4L-R6 consumes the G211C3R4L-R5 GPU timestamp phase probe and emits a candidate resource reuse probe receipt. It keeps the Burn WebGPU matmul baseline and the QW-55A-0-R3 Logical16 KPanel candidate aligned through the same input SSOT and preserves R5 correctness gates.

R6 does not promote a runtime policy and does not declare a performance winner. It records reuse-mode observations, cache hit/miss events, guard status, host phase stats, and GPU timestamp phase stats so later patches can choose a safe optimization target.

## Parent seal

```text
parent_patch_id = G211C3R4L-R5
parent_verdict = PASS_G211C3R4L_R5_GPU_TIMESTAMP_PHASE_PROBE_SEALED
baseline_target_kind = BurnWebGpuMatmul
candidate_target_kind = Logical16FromTile8SoftGroupKPanel
candidate_gpu_timer_source = GpuTimestampQuery
```

## Reuse modes

Required modes:

```text
ColdCreateEveryIteration
PipelineCached
PipelineBuffersCached
PipelineBuffersBindGroupCached
FullCandidateResourceCached
```

R6 PASS requires every fixture to be reported under every required reuse mode.

## Cache observation contract

Required cache observations:

```text
pipeline_cache_hit_count
pipeline_cache_miss_count
bind_group_layout_cache_hit_count
bind_group_layout_cache_miss_count
bind_group_cache_hit_count
bind_group_cache_miss_count
buffer_cache_hit_count
buffer_cache_miss_count
cache_events
```

Cache key domains:

```text
pipeline_cache_key = shader_sha256 + entry_point + workgroup_size + candidate_kernel_kind + storage_layout_version
bind_group_layout_cache_key = binding_count + binding_types + visibility_flags + storage_layout_version
buffer_cache_key = buffer_role + byte_size + usage_flags + alignment + candidate_kernel_kind
```

Bind group reuse is allowed only when A/B/C/control buffer identity is stable.

## Candidate storage layout

Candidate shader storage layout remains the QW-55A-0-R3 four-storage-buffer control_words layout.

```text
binding(0): A atlas
binding(1): B atlas
binding(2): C atlas
binding(3): control_words
```

Forbidden:

```text
candidate fifth storage binding
tile_id_table as separate storage binding
parent R3 candidate shader mutation
timestamp resources as shader storage binding
```

## Timestamp continuity

R6 preserves the R5 timestamp marker coverage.

```text
timestamp_query_created = true
timestamp_query_resolved = true
timestamp_readback_mapped = true
timestamp_period_ns_present = true
timestamp_ticks_resolved = true
timestamp_us_converted = true
missing_timestamp_markers = []
timestamp_marker_coverage_ratio = 1.0
```

## Host phase contract

Each reuse mode records:

```text
host_candidate_total_us
host_pipeline_prepare_us
host_bind_group_layout_prepare_us
host_bind_group_prepare_us
host_buffer_create_us
host_buffer_upload_us
host_command_encode_us
host_queue_submit_us
host_device_poll_us
host_map_async_wait_us
host_readback_decode_us
host_cpu_compare_us
```

## GPU phase contract

Each reuse mode preserves R5 GPU timestamp phases:

```text
gpu_candidate_dispatch_body_us
gpu_candidate_compute_pass_us
gpu_candidate_copy_to_readback_us
gpu_candidate_timestamp_resolve_us
gpu_candidate_encoder_total_us
```

GPU and host timing must remain separate.

```text
gpu_timestamp_timer_source = GpuTimestampQuery
host_timer_source = HostInstant
gpu_host_timing_merged = false
```

## Fixture contract

```text
k_panel_count = 1 -> M=16 N=16 K=8
k_panel_count = 2 -> M=16 N=16 K=16
k_panel_count = 4 -> M=16 N=16 K=32
k_panel_count = 8 -> M=16 N=16 K=64
```

Input SSOT remains unchanged.

```text
same_input_ssot_used = true
logical_a/logical_b generated once
Burn tensors derived from same logical input
Candidate tiles derived from same logical input
```

## Measurement policy

```text
warmup_iterations >= 5
measure_iterations >= 30
outlier_policy = trim_min_max_one_each_if_samples_ge_10
fixture_count = 4
reuse_mode_count = 5
expected_measure_blocks = fixture_count * reuse_mode_count
raw_samples_retained = true
summary_stats_computed = true
```

## Correctness preservation

Every fixture and reuse mode preserves:

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

## Reuse safety gates

```text
output_stale_read_guard_enabled = true
c_buffer_write_observed = true
readback_after_current_submit = true
control_words_fresh_for_fixture = true
tile_id_table_fresh_for_fixture = true
k_panel_count_fresh_for_fixture = true
timestamp_query_indices_not_reused_without_resolve = true
timestamp_readback_contains_current_iteration = true
bind_group_cache_hit_allowed_only_with_stable_buffer_identity = true
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
workspace/runtime/tensorcube/g211c3r4l_r6_resource_reuse_fixture_latest.json
workspace/runtime/tensorcube/g211c3r4l_r6_cache_events_latest.json
workspace/runtime/tensorcube/g211c3r4l_r6_reuse_mode_timing_latest.json
workspace/runtime/tensorcube/g211c3r4l_r6_candidate_resource_reuse_probe_receipt_latest.json
artifacts/g211c3r4l_r6_candidate_resource_reuse_probe_local_manifest.json
```

These files are not committed.

## Audit commands

Default:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r6_candidate_resource_reuse_probe_audit
```

Strict:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r6_candidate_resource_reuse_probe_audit -- --require-native-adapter
```

With fixtures and timing options:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r6_candidate_resource_reuse_probe_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30
```

With explicit reuse modes:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r6_candidate_resource_reuse_probe_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --reuse-modes cold,pipeline,pipeline-buffers,pipeline-buffers-bindgroup,full
```

## PASS verdict

```text
PASS_G211C3R4L_R6_CANDIDATE_RESOURCE_REUSE_PROBE_SEALED
```

PASS means the candidate reuse-mode probe recorded cache events, safety guards, host phase stats, and GPU timestamp phase continuity while parent correctness remained intact. PASS does not mean a runtime cache policy has been adopted.

## Failure conditions

```text
FAIL: parent_patch_id != G211C3R4L-R5
FAIL: parent R5 verdict is not PASS
FAIL: baseline_target_kind != BurnWebGpuMatmul
FAIL: candidate_target_kind != Logical16FromTile8SoftGroupKPanel
FAIL: same_input_ssot_used = false
FAIL: cpu_reference_used_as_benchmark_baseline = true
FAIL: required reuse mode missing
FAIL: cache_events_recorded = false
FAIL: cache_safety_gates_passed = false
FAIL: stale_output_guard_passed = false
FAIL: control_words_freshness_guard_passed = false
FAIL: timestamp_freshness_guard_passed = false
FAIL: bind_group_identity_guard_passed = false
FAIL: bind group cache hit with unstable buffer identity
FAIL: stale output readback detected
FAIL: control_words not refreshed for fixture
FAIL: timestamp readback contains stale iteration data
FAIL: timestamp markers missing
FAIL: timestamp marker coverage < 1.0
FAIL: gpu phase stats empty
FAIL: host phase stats empty
FAIL: burn correctness mismatch > 0
FAIL: candidate correctness mismatch > 0
FAIL: candidate vs Burn mismatch > 0
FAIL: performance_winner_declared = true
FAIL: runtime_inference_replacement_allowed = true
FAIL: backend_policy_connection_allowed = true
FAIL: hardware_tensorcore_claimed = true
FAIL: candidate uses fifth storage binding
```
