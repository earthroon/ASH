# ASH-BASETRAIN-GPU-70K-G211C3R4C

## Repeated Dispatch Batch Timing Crosscheck / Small Shape Amortization Probe / No Runtime Splice No Promotion Reopen

Seal: Small Shape Batch Timing Evidence Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4C` consumes the G211C3R4B dispatch-only timing probe outputs as its entry authority and preserves the G211C3 `STOP_PERF_LOSS` result.

`70K-G211C3R4C` may only pass when G211C3R4B PASS is present, the G211C3R4B next entry packet to G211C3R4C is present, `timestamp_query_status = TIMESTAMP_QUERY_AVAILABLE`, `dispatch_timing_verdict = DISPATCH_ONLY_TIMING_CAPTURED`, all required B0-B5 shapes were measured in R4B, B0/B1 batch timing is captured in R4C, parity remains pass, the G211C3 promotion stop is retained, and no G211C4 entry packet exists.

`70K-G211C3R4C` must not mutate the TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not implement TensorCube kernel optimization, must not rerun promotion, and must not claim TensorCore usage, speedup, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R4B
Dispatch Only Timing Probe /
GPU Timestamp Dispatch Timing Split /
No Runtime Splice No Promotion Reopen
```

Required predecessor evidence:

```text
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_DISPATCH_ONLY_TIMING_PROBE.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_DISPATCH_ONLY_TIMING_MATRIX.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_READBACK_POLLUTION_SPLIT.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_NEXT_ENTRY_PACKET_G211C3R4C.json
artifacts/g211c3r4b/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4B.txt
```

Required G211C3 evidence:

```text
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_TENSORCUBE_MICROBENCH_BASELINE.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_SHAPE_BENCHMARK_MATRIX.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_PROMOTION_STOP_PACKET.json
```

Forbidden evidence:

```text
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r3/ASH_BASETRAIN_GPU_70K_G211C3R3_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_NEXT_ENTRY_PACKET_G211C4.json
```

## Purpose

G211C3R4C measures repeated dispatch batch timing for small shapes B0 and B1 using the GPU timestamp path established by G211C3R4A and verified by G211C3R4B.

G211C3R4C proves only this:

```text
G211C3 STOP_PERF_LOSS was preserved
G211C3R4B dispatch-only timing was accepted as entry authority
B0/B1 repeated dispatch batch timing was measured
batch_count = 1, 4, 16, 64, 256 was covered
selected_batch_count was recorded
small shape recovery delta was calculated
parity remained pass
runtime splice and promotion remained closed
```

G211C3R4C does not optimize TensorCube. G211C3R4C does not rerun benchmark promotion. G211C3R4C does not authorize G211C4.

## Required Batch Probe Shapes

```text
B0 = [8, 8, 8]
B1 = [16, 16, 8]
```

Required reference shape coverage from R4B remains:

```text
B0 = [8, 8, 8]
B1 = [16, 16, 8]
B2 = [16, 16, 64]
B3 = [64, 64, 64]
B4 = [128, 128, 128]
B5 = [17, 31, 65]
```

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4c_repeated_dispatch_batch_timing.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4c_repeated_dispatch_batch_timing
```

Alternative command from `crates/base_train`:

```powershell
cargo run --bin ash_basetrain_gpu_70k_g211c3r4c_repeated_dispatch_batch_timing
```

Optional arguments:

```text
--g211c3-dir artifacts/g211c3
--g211c3r4a-dir artifacts/g211c3r4a
--g211c3r4b-dir artifacts/g211c3r4b
--out-dir artifacts/g211c3r4c
--warmup-iterations 20
--measured-iterations 100
--batch-counts 1,4,16,64,256
--selected-batch-count 256
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4C_REPEATED_DISPATCH_BATCH_TIMING
```

## Batch Timing Contract

G211C3R4C uses GPU timestamp query as timing authority. It must not silently fall back to CPU wall-clock timing.

Required batch counts:

```text
1, 4, 16, 64, 256
```

For each required batch probe shape and each path:

```text
baseline
tensorcube_candidate
```

record:

```text
single_dispatch_gpu_ms
batched_dispatch_total_gpu_ms
batched_dispatch_amortized_gpu_ms
batched_dispatch_p50_ms
batched_dispatch_p95_ms
batched_dispatch_mean_ms
batched_dispatch_min_ms
batched_dispatch_max_ms
batched_dispatch_stddev_ms
```

Correctness policy:

```text
candidate_vs_cpu_parity_pass = true
candidate_vs_baseline_parity_pass = true
parity_sample_policy = FINAL_DISPATCH_OUTPUT_ONLY
```

## Derived Metrics

```text
amortization_gain_ratio = single_dispatch_gpu_p50_ms / batched_dispatch_amortized_gpu_p50_ms
single_dispatch_speedup_ratio = baseline_single_dispatch_p50_ms / candidate_single_dispatch_p50_ms
batched_dispatch_speedup_ratio = baseline_batched_amortized_p50_ms / candidate_batched_amortized_p50_ms
candidate_recovery_delta = batched_dispatch_speedup_ratio - single_dispatch_speedup_ratio
```

Default selected batch count:

```text
selected_batch_count = 256
```

## Verdict Values

G211C3R4C must produce exactly one batch timing verdict.

```text
BATCH_AMORTIZATION_CAPTURED
SMALL_SHAPE_DISPATCH_OVERHEAD_LIKELY
SMALL_SHAPE_KERNEL_OR_TILE_LOSS_REMAINS
BATCH_TIMESTAMP_UNSTABLE
BATCH_PARITY_FAILED
BATCH_MATRIX_INCOMPLETE
INCONCLUSIVE
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r4c` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_REPEATED_DISPATCH_BATCH_TIMING.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_SMALL_SHAPE_AMORTIZATION_MATRIX.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_BATCH_RECOVERY_SUMMARY.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_NEXT_ENTRY_PACKET_G211C3R4D.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_BAKE_MANIFEST.json
artifacts/g211c3r4c/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4C.txt
```

Forbidden output:

```text
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_NEXT_ENTRY_PACKET_G211C4.json
```

## Main Receipt Required Fields

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-70K-G211C3R4C",
  "patch_name": "Repeated Dispatch Batch Timing Crosscheck",
  "status": "PASS_ASH_BASETRAIN_GPU_70K_G211C3R4C_REPEATED_DISPATCH_BATCH_TIMING",
  "predecessor": "ASH-BASETRAIN-GPU-70K-G211C3R4B",
  "g211c3r4b_entry_verified": true,
  "g211c3_microbench_verdict": "STOP_PERF_LOSS",
  "timestamp_query_status": "TIMESTAMP_QUERY_AVAILABLE",
  "dispatch_timing_verdict_from_r4b": "DISPATCH_ONLY_TIMING_CAPTURED",
  "batch_timing_verdict": "BATCH_AMORTIZATION_CAPTURED",
  "promotion_stop_retained": true,
  "runtime_splice_allowed": false,
  "promotion_allowed": false,
  "g211c4_entry_generated": false
}
```

## Next Gate

G211C3R4C routes to G211C3R4D, not G211C4.

```text
ASH-BASETRAIN-GPU-70K-G211C3R4D
Pipeline And Bind Group Reuse Split /
Setup Overhead Isolation Probe /
No Runtime Splice No Promotion Reopen
```

## PASS Criteria

```text
PASS-01 G211C3R4B PASS marker found
PASS-02 G211C3R4B next entry packet found
PASS-03 timestamp_query_status = TIMESTAMP_QUERY_AVAILABLE
PASS-04 dispatch_timing_verdict = DISPATCH_ONLY_TIMING_CAPTURED
PASS-05 G211C3 STOP_PERF_LOSS retained
PASS-06 G211C4 entry packet absent
PASS-07 required batch probe shapes B0/B1 present
PASS-08 baseline repeated dispatch batch timing recorded for B0/B1
PASS-09 candidate repeated dispatch batch timing recorded for B0/B1
PASS-10 batch counts include 1, 4, 16, 64, 256
PASS-11 selected batch count recorded
PASS-12 timestamp stability audit written
PASS-13 small shape amortization matrix written
PASS-14 batch recovery summary written
PASS-15 parity remains pass
PASS-16 batch timing verdict selected exactly once
PASS-17 promotion stop retained
PASS-18 runtime_splice_allowed=false
PASS-19 promotion_allowed=false
PASS-20 G211C3R4D entry packet generated
PASS-21 G211C4 entry packet not generated
PASS-22 forbidden mutation seal passed
PASS-23 PASS marker printed
```

## BLOCKED Codes

```text
ERR_70K_G211C3R4C_G211C3R4B_PASS_MARKER_MISSING
ERR_70K_G211C3R4C_G211C3R4B_ENTRY_PACKET_MISSING
ERR_70K_G211C3R4C_TIMESTAMP_NOT_AVAILABLE
ERR_70K_G211C3R4C_R4B_DISPATCH_TIMING_NOT_CAPTURED
ERR_70K_G211C3R4C_REQUIRED_BATCH_SHAPE_MISSING
ERR_70K_G211C3R4C_BATCH_TIMESTAMP_UNSTABLE
ERR_70K_G211C3R4C_PARITY_FAILED
ERR_70K_G211C3R4C_UNEXPECTED_G211C4_ENTRY_PACKET
ERR_70K_G211C3R4C_RUNTIME_MUTATION_DETECTED
```

## PASS Meaning

PASS means G211C3R4C captured or explicitly audited repeated dispatch batch timing for small shapes and determined whether candidate loss is reduced by dispatch batching.

PASS does not mean TensorCube is faster. PASS does not mean TensorCube timing hygiene is fully repaired. PASS does not mean TensorCube optimization has been applied. PASS does not mean TensorCube promotion is reopened. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean production acceleration exists. PASS does not mean TensorCore is used.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4C repeated dispatch batch timing

- Add repeated dispatch batch timing crosscheck gate
- Require G211C3R4B dispatch-only timestamp timing as entry authority
- Probe B0/B1 small-shape amortization across batch counts
- Measure baseline and TensorCube candidate batched dispatch timing
- Compute candidate recovery delta and small-shape amortization class
- Preserve G211C3 STOP_PERF_LOSS and promotion stop
- Route to G211C3R4D pipeline and bind group reuse split
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
