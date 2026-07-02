# ASH-BASETRAIN-GPU-70K-G211C3R2

## TensorCube Targeted Microbench Hygiene And Overhead Isolation / Pipeline BindGroup Readback Split / No Runtime Splice No Promotion Reopen

Seal: Overhead Isolation Evidence Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R2` consumes the G211C3R1 perf loss attribution outputs as its entry authority and preserves the G211C3 `STOP_PERF_LOSS` result.

`70K-G211C3R2` may only pass when G211C3R1 PASS is present, the G211C3R1 entry packet to G211C3R2 is present, the original G211C3 microbench receipt and shape matrix are present, the G211C3 promotion stop is retained, and no G211C4 entry packet exists.

`70K-G211C3R2` must not mutate the TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not claim TensorCore usage, speedup, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R1
TensorCube Perf Loss Attribution /
Shape Benchmark Matrix Bottleneck Split /
No Runtime Splice No Promotion Reopen
```

Required predecessor evidence:

```text
artifacts/g211c3r1/ASH_BASETRAIN_GPU_70K_G211C3R1_PERF_LOSS_ATTRIBUTION.json
artifacts/g211c3r1/ASH_BASETRAIN_GPU_70K_G211C3R1_SHAPE_BOTTLENECK_SPLIT.json
artifacts/g211c3r1/ASH_BASETRAIN_GPU_70K_G211C3R1_MEASUREMENT_HYGIENE_AUDIT.json
artifacts/g211c3r1/ASH_BASETRAIN_GPU_70K_G211C3R1_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r1/ASH_BASETRAIN_GPU_70K_G211C3R1_NEXT_ENTRY_PACKET_G211C3R2.json
artifacts/g211c3r1/PASS_ASH_BASETRAIN_GPU_70K_G211C3R1.txt
```

Required original G211C3 evidence:

```text
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_TENSORCUBE_MICROBENCH_BASELINE.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_SHAPE_BENCHMARK_MATRIX.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_PROMOTION_STOP_PACKET.json
```

Forbidden evidence:

```text
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_NEXT_ENTRY_PACKET_G211C4.json
```

## Purpose

G211C3R2 isolates whether the observed G211C3 perf loss is likely caused by TensorCube kernel compute itself or by measurement/setup overhead.

G211C3R2 proves only this:

```text
G211C3 STOP_PERF_LOSS was preserved
G211C3R1 perf loss attribution was accepted as entry authority
pipeline and bind group reuse hygiene was audited
readback and poll timing hygiene was audited
dispatch-only timing availability was recorded
small-shape amortization need was recorded
odd-shape padding overhead need was recorded
runtime splice and promotion remained closed
```

G211C3R2 does not fix performance. G211C3R2 does not reopen TensorCube promotion. G211C3R2 does not authorize G211C4.

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r2_tensorcube_microbench_hygiene_overhead_isolation.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r2_tensorcube_microbench_hygiene_overhead_isolation
```

Alternative command from `crates/base_train`:

```powershell
cargo run --bin ash_basetrain_gpu_70k_g211c3r2_tensorcube_microbench_hygiene_overhead_isolation
```

Optional arguments:

```text
--g211c3-dir artifacts/g211c3
--g211c3r1-dir artifacts/g211c3r1
--out-dir artifacts/g211c3r2
--warmup-iterations 20
--measured-iterations 100
--batch-dispatch-count 256
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R2_OVERHEAD_ISOLATION
```

## Required Shapes

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

## Isolation Axes

G211C3R2 records or explicitly marks unavailable:

```text
pipeline_layout_create_ms
shader_module_create_ms
compute_pipeline_create_ms
bind_group_layout_create_ms
bind_group_create_ms
pipeline_reuse
bind_group_reuse
dispatch_only_p50_ms
dispatch_only_p95_ms
dispatch_readback_p50_ms
dispatch_readback_p95_ms
copy_to_readback_ms
device_poll_wait_ms
map_async_wait_ms
readback_decode_ms
timestamp_query_supported
timestamp_query_used
cpu_wall_clock_timing_used
small_shape_batch_timing_recorded
odd_shape_padding_isolation_recorded
```

If direct dispatch-only timing or timestamp query timing is unavailable, the gate must not invent values. It must record `dispatch_only_timing_mode = UNAVAILABLE` or `APPROXIMATED_BY_BATCH_AMORTIZATION`.

## Derived Metrics

```text
setup_cost_ms = pipeline_layout_create_ms + shader_module_create_ms + compute_pipeline_create_ms + bind_group_layout_create_ms + bind_group_create_ms
setup_cost_ratio = setup_cost_ms / dispatch_readback_p50_ms
readback_cost_ms = copy_to_readback_ms + device_poll_wait_ms + map_async_wait_ms + readback_decode_ms
readback_cost_ratio = readback_cost_ms / dispatch_readback_p50_ms
compute_isolation_ratio = dispatch_only_p50_ms / dispatch_readback_p50_ms
amortization_gain_ratio = single_dispatch_latency_ms / repeated_dispatch_amortized_ms
padding_cost_ratio = padding_guard_overhead_ms / odd_shape_original_ms
```

Unavailable source fields must produce `null` values or explicit `UNAVAILABLE` status, not fabricated timing numbers.

## Hygiene Verdict Values

```text
OVERHEAD_ISOLATED_SETUP_DOMINANT
OVERHEAD_ISOLATED_READBACK_DOMINANT
OVERHEAD_ISOLATED_DISPATCH_AMORTIZATION_DOMINANT
OVERHEAD_ISOLATED_PADDING_DOMINANT
KERNEL_COMPUTE_LOSS_CONFIRMED
MEASUREMENT_HYGIENE_INCOMPLETE
INCONCLUSIVE
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r2` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_OVERHEAD_ISOLATION.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_TIMING_COMPONENT_MATRIX.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_SMALL_SHAPE_BATCH_TIMING.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_ODD_SHAPE_PADDING_ISOLATION.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_MEASUREMENT_HYGIENE_AUDIT.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_NEXT_ENTRY_PACKET_G211C3R3.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_BAKE_MANIFEST.json
artifacts/g211c3r2/PASS_ASH_BASETRAIN_GPU_70K_G211C3R2.txt
```

Forbidden output:

```text
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_NEXT_ENTRY_PACKET_G211C4.json
```

## Main Receipt Required Fields

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-70K-G211C3R2",
  "patch_name": "TensorCube Targeted Microbench Hygiene And Overhead Isolation",
  "status": "PASS_ASH_BASETRAIN_GPU_70K_G211C3R2_OVERHEAD_ISOLATION",
  "predecessor": "ASH-BASETRAIN-GPU-70K-G211C3R1",
  "g211c3r1_entry_verified": true,
  "g211c3_microbench_verdict": "STOP_PERF_LOSS",
  "promotion_stop_retained": true,
  "runtime_splice_allowed": false,
  "promotion_allowed": false,
  "g211c4_entry_generated": false,
  "summary": {
    "hygiene_verdict": "MEASUREMENT_HYGIENE_INCOMPLETE",
    "primary_overhead_class": "INCONCLUSIVE",
    "kernel_compute_loss_confirmed": false,
    "measurement_pollution_confirmed": false
  }
}
```

## G211C3R3 Entry Packet

G211C3R2 always routes to G211C3R3, not G211C4.

```text
ASH-BASETRAIN-GPU-70K-G211C3R3
TensorCube Targeted Optimization Candidate Plan /
Overhead Verdict To Patch Queue /
No Runtime Splice No Promotion Reopen
```

## PASS Criteria

```text
PASS-01 G211C3R1 PASS marker found
PASS-02 G211C3R1 next entry packet found
PASS-03 G211C3 original microbench receipt found
PASS-04 G211C3 original shape matrix found
PASS-05 G211C3 verdict STOP_PERF_LOSS retained
PASS-06 G211C4 entry packet absent
PASS-07 all required shapes B0-B5 present
PASS-08 pipeline reuse recorded or explicitly unavailable
PASS-09 bind group reuse recorded or explicitly unavailable
PASS-10 dispatch-only timing recorded or explicitly unavailable
PASS-11 dispatch plus readback timing recorded
PASS-12 readback/poll/map timing recorded or explicitly unavailable
PASS-13 timestamp query policy recorded
PASS-14 small shape batch timing recorded or explicitly unavailable
PASS-15 odd shape padding isolation recorded or explicitly unavailable
PASS-16 timing component matrix written
PASS-17 hygiene verdict written
PASS-18 promotion stop retained
PASS-19 runtime_splice_allowed=false
PASS-20 promotion_allowed=false
PASS-21 G211C3R3 entry packet generated
PASS-22 G211C4 entry packet not generated
PASS-23 forbidden mutation seal passed
PASS-24 PASS marker printed
```

## BLOCKED Codes

```text
ERR_70K_G211C3R2_G211C3R1_PASS_MARKER_MISSING
ERR_70K_G211C3R2_G211C3R1_ENTRY_PACKET_MISSING
ERR_70K_G211C3R2_G211C3_MATRIX_MISSING
ERR_70K_G211C3R2_NOT_STOP_PERF_LOSS
ERR_70K_G211C3R2_UNEXPECTED_G211C4_ENTRY_PACKET
ERR_70K_G211C3R2_REQUIRED_SHAPE_MISSING
ERR_70K_G211C3R2_PARITY_NOT_PASS
ERR_70K_G211C3R2_RUNTIME_MUTATION_DETECTED
```

## PASS Meaning

PASS means G211C3R2 separated or explicitly audited TensorCube microbench overhead components after C3 STOP_PERF_LOSS, preserved the promotion stop, and routed to targeted optimization planning.

PASS does not mean TensorCube is faster. PASS does not mean TensorCube promotion is reopened. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean production acceleration exists. PASS does not mean TensorCore is used.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R2 tensorcube microbench overhead isolation

- Add targeted microbench hygiene and overhead isolation gate
- Require G211C3R1 perf loss attribution as entry authority
- Audit pipeline setup, bind group setup, dispatch-only, dispatch+readback, readback/poll/map timing
- Record unavailable direct timing fields explicitly instead of inventing numbers
- Add small-shape and odd-shape overhead isolation receipts
- Route to G211C3R3 targeted optimization candidate plan
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
