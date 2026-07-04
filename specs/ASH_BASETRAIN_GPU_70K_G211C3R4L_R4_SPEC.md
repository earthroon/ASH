# G211C3R4L-R4
## Benchmark Timing Stabilization / Upload-Dispatch-Readback Phase Split Seal

## Scope

G211C3R4L-R4 consumes the G211C3R4L-R3 benchmark-target-alignment receipt and emits a timing phase split receipt. It keeps Burn WebGPU matmul and the QW-55A-0-R3 Logical16 KPanel candidate on the same input SSOT and same native adapter/device alignment.

R4 does not declare a performance winner. It decomposes measured totals into named timing phases and records per-phase samples/statistics so later patches can choose optimization targets without changing runtime behavior.

## Parent seal

```text
parent_patch_id = G211C3R4L-R3
parent_verdict = PASS_G211C3R4L_R3_BENCHMARK_TARGET_ALIGNMENT_SEALED
baseline_target_kind = BurnWebGpuMatmul
candidate_target_kind = Logical16FromTile8SoftGroupKPanel
```

## Required phases

Common:

```text
fixture_build_us
input_projection_us
cpu_reference_us
receipt_serialization_us
```

Burn:

```text
burn_tensor_create_us
burn_upload_or_materialize_us
burn_matmul_encode_or_eval_us
burn_queue_submit_or_eval_wait_us
burn_readback_us
burn_cpu_compare_us
```

Candidate:

```text
candidate_tile_pack_us
candidate_buffer_create_us
candidate_upload_us
candidate_pipeline_prepare_us
candidate_bind_group_prepare_us
candidate_dispatch_encode_us
candidate_queue_submit_us
candidate_device_poll_us
candidate_map_async_us
candidate_readback_decode_us
candidate_cpu_compare_us
```

## Measurement policy

```text
warmup_iterations >= 5
measure_iterations >= 30
timer_source = HostInstantPhaseSplitFromParentR3 | GpuTimestampQuery | HostInstant
outlier_policy = trim_min_max_one_each_if_samples_ge_10
```

R4 may use coarse host-derived phase splits when Burn internals expose only aggregate matmul/eval/readback boundaries. The receipt must declare the timer source and must not claim a performance winner.

## Correctness preservation

The parent R3 comparisons remain required:

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
```

## Candidate storage layout

Candidate path must keep the QW-55A-0-R3 four-storage-buffer control_words layout.

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
```

## Local artifacts

Generated locally only:

```text
workspace/runtime/tensorcube/g211c3r4l_r4_timing_fixture_latest.json
workspace/runtime/tensorcube/g211c3r4l_r4_burn_phase_timing_latest.json
workspace/runtime/tensorcube/g211c3r4l_r4_candidate_phase_timing_latest.json
workspace/runtime/tensorcube/g211c3r4l_r4_timing_phase_split_receipt_latest.json
artifacts/g211c3r4l_r4_benchmark_timing_phase_split_local_manifest.json
```

These files are not committed.

## Audit commands

Default:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r4_benchmark_timing_phase_split_audit
```

Strict:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r4_benchmark_timing_phase_split_audit -- --require-native-adapter
```

With fixtures and timing options:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r4_benchmark_timing_phase_split_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30
```

## PASS verdict

```text
PASS_G211C3R4L_R4_BENCHMARK_TIMING_PHASE_SPLIT_SEALED
```

PASS means timing phases and statistics were recorded while R3 target alignment and correctness remained intact. PASS does not mean the Logical16 candidate is faster than Burn.

## Failure conditions

```text
FAIL: parent_patch_id != G211C3R4L-R3
FAIL: parent R3 verdict is not PASS
FAIL: baseline_target_kind != BurnWebGpuMatmul
FAIL: candidate_target_kind != Logical16FromTile8SoftGroupKPanel
FAIL: same_input_ssot_used = false
FAIL: cpu_reference_used_as_benchmark_baseline = true
FAIL: burn correctness mismatch > 0
FAIL: candidate correctness mismatch > 0
FAIL: candidate vs Burn mismatch > 0
FAIL: burn_phase_stats empty
FAIL: candidate_phase_stats empty
FAIL: timing_samples_recorded = false
FAIL: phase_stats_computed = false
FAIL: phase_sum_check_passed = false
FAIL: performance_winner_declared = true
FAIL: runtime_inference_replacement_allowed = true
FAIL: backend_policy_connection_allowed = true
FAIL: hardware_tensorcore_claimed = true
FAIL: candidate uses fifth storage binding
```
