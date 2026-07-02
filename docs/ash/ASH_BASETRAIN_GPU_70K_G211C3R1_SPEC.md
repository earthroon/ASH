# ASH-BASETRAIN-GPU-70K-G211C3R1

## TensorCube Perf Loss Attribution / Shape Benchmark Matrix Bottleneck Split / No Runtime Splice No Promotion Reopen

Seal: Perf Loss Attribution Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R1` consumes the G211C3 TensorCube microbench baseline outputs as its only entry authority.

`70K-G211C3R1` may only pass when G211C3 completed with `microbench_verdict = STOP_PERF_LOSS`, the G211C3 shape benchmark matrix is present, all required shapes B0-B5 are present, parity remained pass, and no G211C4 entry packet was generated.

`70K-G211C3R1` must not mutate the TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not claim TensorCore usage, speedup, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3
TensorCube Microbench Baseline /
Burn Matmul Versus TensorCube Candidate /
Perf Win Required For Further Promotion
```

Required predecessor evidence:

```text
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_TENSORCUBE_MICROBENCH_BASELINE.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_SHAPE_BENCHMARK_MATRIX.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_PROMOTION_STOP_PACKET.json
artifacts/g211c3/PASS_ASH_BASETRAIN_GPU_70K_G211C3.txt
```

Forbidden predecessor evidence:

```text
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_NEXT_ENTRY_PACKET_G211C4.json
```

If a G211C4 entry packet exists while G211C3 verdict is `STOP_PERF_LOSS`, G211C3R1 must fail with `ERR_70K_G211C3R1_UNEXPECTED_G211C4_ENTRY_PACKET`.

## Purpose

G211C3R1 explains why G211C3 stopped promotion. It does not erase the stop condition.

G211C3R1 proves only this:

```text
G211C3 STOP_PERF_LOSS was preserved
shape benchmark matrix was read
shape-level regressions were identified
bottleneck candidates were assigned with evidence levels
measurement hygiene gaps were recorded
runtime splice and promotion remained closed
```

G211C3R1 does not reopen TensorCube promotion. G211C3R1 does not authorize G211C4. G211C3R1 does not rerun production inference.

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r1_tensorcube_perf_loss_attribution.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r1_tensorcube_perf_loss_attribution
```

Alternative command from `crates/base_train`:

```powershell
cargo run --bin ash_basetrain_gpu_70k_g211c3r1_tensorcube_perf_loss_attribution
```

Optional arguments:

```text
--g211c3-dir artifacts/g211c3
--out-dir artifacts/g211c3r1
--require-stop-perf-loss true
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R1_PERF_LOSS_ATTRIBUTION
```

## Required Shape Matrix

Required shape IDs:

```text
B0 = [8, 8, 8]
B1 = [16, 16, 8]
B2 = [16, 16, 64]
B3 = [64, 64, 64]
B4 = [128, 128, 128]
B5 = [17, 31, 65]
```

Shape classes:

```text
B0 [8,8,8]       -> SMALL_SHAPE
B1 [16,16,8]     -> SMALL_SHAPE
B2 [16,16,64]    -> K_LOOP_HEAVY_SHAPE
B3 [64,64,64]    -> MID_SQUARE_SHAPE
B4 [128,128,128] -> LARGE_SQUARE_SHAPE
B5 [17,31,65]    -> ODD_EDGE_SHAPE
```

Each required shape entry must contain, directly or derivably:

```text
baseline.p50_ms
baseline.p95_ms
baseline.max_ms
baseline.mean_ms
candidate.p50_ms
candidate.p95_ms
candidate.max_ms
candidate.mean_ms
comparison.candidate_speedup_ratio_p50
comparison.candidate_speedup_ratio_p95
comparison.latency_regression
comparison.perf_win
parity.candidate_vs_cpu_parity_pass
parity.candidate_vs_baseline_parity_pass
```

## Attribution Axes

Bottleneck classes:

```text
DISPATCH_OVERHEAD_DOMINANT
PIPELINE_OR_BINDGROUP_SETUP_INCLUDED
READBACK_OR_POLL_BARRIER_INCLUDED
TILE_UTILIZATION_LOSS
K_LOOP_INEFFICIENCY
ODD_SHAPE_PADDING_OVERHEAD
MEMORY_ACCESS_OR_COALESCING_LOSS
BASELINE_ADVANTAGE_UNATTRIBUTED
MEASUREMENT_NOISE
INCONCLUSIVE
```

Evidence levels:

```text
CONFIRMED
LIKELY
POSSIBLE
INCONCLUSIVE
```

`CONFIRMED` requires explicit diagnostic fields. Matrix-only inference must use `LIKELY` or `POSSIBLE`.

## Derived Metrics

For every shape:

```text
speedup_delta = candidate_speedup_ratio_p50 - 1.0
regression_percent = max(0.0, (1.0 - candidate_speedup_ratio_p50) * 100.0)
baseline_tail_ratio = baseline_p95_ms / baseline_p50_ms
candidate_tail_ratio = candidate_p95_ms / candidate_p50_ms
tail_divergence = candidate_tail_ratio - baseline_tail_ratio
```

Global geomean contribution:

```text
mean_log_speedup = mean(ln(candidate_speedup_ratio_p50 for B0-B5))
loss_contribution_log = ln(candidate_speedup_ratio_p50) - mean_log_speedup
```

The most negative `loss_contribution_log` identifies the largest log loss contributor.

## Attribution Rules

Small shape loss:

```text
if shape_class = SMALL_SHAPE and speedup_ratio_p50 < 1.0:
  bottleneck_class = DISPATCH_OVERHEAD_DOMINANT
  evidence_level = LIKELY
```

Pipeline or bind group setup uncertainty:

```text
if pipeline_reuse_recorded = false or bind_group_reuse_recorded = false:
  bottleneck_class = PIPELINE_OR_BINDGROUP_SETUP_INCLUDED
  evidence_level = POSSIBLE
```

Readback or poll barrier:

```text
if timing_mode contains readback or timing_mode contains poll:
  bottleneck_class = READBACK_OR_POLL_BARRIER_INCLUDED
  evidence_level = CONFIRMED
```

Tile utilization loss:

```text
if M % 8 != 0 or N % 8 != 0:
  bottleneck_class = TILE_UTILIZATION_LOSS
  evidence_level = LIKELY
```

Odd shape padding overhead:

```text
if shape_id = B5 and speedup_ratio_p50 < 1.0:
  bottleneck_class = ODD_SHAPE_PADDING_OVERHEAD
  evidence_level = LIKELY
```

K-loop inefficiency:

```text
if shape_class = K_LOOP_HEAVY_SHAPE and speedup_ratio_p50 < 1.0:
  bottleneck_class = K_LOOP_INEFFICIENCY
  evidence_level = LIKELY
```

Memory or coalescing loss:

```text
if shape_class = LARGE_SQUARE_SHAPE and speedup_ratio_p50 < 1.0 and tail_divergence > 0.0:
  bottleneck_class = MEMORY_ACCESS_OR_COALESCING_LOSS
  evidence_level = POSSIBLE
```

Measurement noise:

```text
if abs(speedup_ratio_p50 - 1.0) < 0.01:
  bottleneck_class = MEASUREMENT_NOISE
  evidence_level = POSSIBLE
```

If no rule applies to a regressed shape:

```text
bottleneck_class = BASELINE_ADVANTAGE_UNATTRIBUTED
evidence_level = INCONCLUSIVE
```

## Local Outputs

The baked package must not contain prebaked `artifacts/g211c3r1` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r1/ASH_BASETRAIN_GPU_70K_G211C3R1_PERF_LOSS_ATTRIBUTION.json
artifacts/g211c3r1/ASH_BASETRAIN_GPU_70K_G211C3R1_SHAPE_BOTTLENECK_SPLIT.json
artifacts/g211c3r1/ASH_BASETRAIN_GPU_70K_G211C3R1_MEASUREMENT_HYGIENE_AUDIT.json
artifacts/g211c3r1/ASH_BASETRAIN_GPU_70K_G211C3R1_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r1/ASH_BASETRAIN_GPU_70K_G211C3R1_NEXT_ENTRY_PACKET_G211C3R2.json
artifacts/g211c3r1/ASH_BASETRAIN_GPU_70K_G211C3R1_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r1/ASH_BASETRAIN_GPU_70K_G211C3R1_BAKE_MANIFEST.json
artifacts/g211c3r1/PASS_ASH_BASETRAIN_GPU_70K_G211C3R1.txt
```

No G211C4 entry packet may be generated.

## Main Attribution Receipt

Main receipt must include:

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-70K-G211C3R1",
  "patch_name": "TensorCube Perf Loss Attribution",
  "status": "PASS_ASH_BASETRAIN_GPU_70K_G211C3R1_PERF_LOSS_ATTRIBUTION",
  "predecessor": "ASH-BASETRAIN-GPU-70K-G211C3",
  "g211c3_entry_verified": true,
  "g211c3_microbench_verdict": "STOP_PERF_LOSS",
  "promotion_stop_retained": true,
  "runtime_splice_allowed": false,
  "promotion_allowed": false,
  "observed_perf": {
    "geomean_speedup_ratio": 0.0,
    "min_speedup_ratio": 0.0,
    "shape_count": 6,
    "parity_pass": true
  },
  "attribution": {
    "attribution_status": "PERF_LOSS_ATTRIBUTED",
    "primary_bottleneck_class": "INCONCLUSIVE",
    "secondary_bottleneck_classes": [],
    "worst_shape_by_p50": "",
    "worst_shape_by_p95": "",
    "largest_log_loss_contributor": "",
    "candidate_tail_instability_possible": false
  }
}
```

## Measurement Hygiene Audit

The hygiene audit must record whether G211C3 captured:

```text
same_input_policy_pass
same_adapter_policy_pass
warmup_iterations_present
measured_iterations_present
baseline_path_resolved
candidate_path_resolved
pipeline_reuse_recorded
bind_group_reuse_recorded
readback_included_recorded
timestamp_query_used_recorded
dispatch_only_timing_recorded
```

If overhead isolation fields are missing, `hygiene_verdict = MISSING_OVERHEAD_ISOLATION_FIELDS` and G211C3R2 must be required.

## G211C3R2 Entry Packet

G211C3R1 always routes to G211C3R2, not G211C4.

```text
ASH-BASETRAIN-GPU-70K-G211C3R2
TensorCube Targeted Microbench Hygiene And Overhead Isolation /
Pipeline BindGroup Readback Split /
No Runtime Splice No Promotion Reopen
```

## PASS Criteria

```text
PASS-01 G211C3 PASS marker found
PASS-02 G211C3 microbench receipt found
PASS-03 G211C3 shape benchmark matrix found
PASS-04 microbench_verdict = STOP_PERF_LOSS
PASS-05 G211C4 entry packet absent
PASS-06 all required shapes B0-B5 present
PASS-07 parity remains pass
PASS-08 shape speedup deltas computed
PASS-09 geomean loss contribution computed
PASS-10 worst shape by p50 identified
PASS-11 worst shape by p95 identified
PASS-12 bottleneck candidates assigned
PASS-13 measurement hygiene audit written
PASS-14 promotion stop retained
PASS-15 runtime_splice_allowed=false
PASS-16 promotion_allowed=false
PASS-17 G211C3R2 entry packet generated
PASS-18 G211C4 entry packet not generated
PASS-19 forbidden mutation seal passed
PASS-20 PASS marker printed
```

## BLOCKED Codes

```text
ERR_70K_G211C3R1_G211C3_PASS_MARKER_MISSING
ERR_70K_G211C3R1_MICROBENCH_RECEIPT_MISSING
ERR_70K_G211C3R1_SHAPE_MATRIX_MISSING
ERR_70K_G211C3R1_NOT_STOP_PERF_LOSS
ERR_70K_G211C3R1_UNEXPECTED_G211C4_ENTRY_PACKET
ERR_70K_G211C3R1_REQUIRED_SHAPE_MISSING
ERR_70K_G211C3R1_PARITY_NOT_PASS
ERR_70K_G211C3R1_RUNTIME_MUTATION_DETECTED
```

## PASS Meaning

PASS means G211C3 STOP_PERF_LOSS was analyzed against the shape benchmark matrix, bottleneck candidates were attributed with evidence levels, measurement hygiene gaps were recorded, and promotion stop remained active.

PASS does not mean TensorCube is faster. PASS does not mean TensorCube promotion is reopened. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean production acceleration exists.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R1 tensorcube perf loss attribution

- Add TensorCube perf loss attribution gate
- Require G211C3 STOP_PERF_LOSS as entry authority
- Split shape benchmark matrix into bottleneck candidates
- Compute shape speedup deltas, regression percent, log loss contribution, and tail divergence
- Audit measurement hygiene for pipeline reuse, bind group reuse, readback timing, and timestamp policy
- Route to G211C3R2 targeted overhead isolation
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
