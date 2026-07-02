# ASH-BASETRAIN-GPU-70K-G211C3R4B

## Dispatch Only Timing Probe / GPU Timestamp Dispatch Timing Split / No Runtime Splice No Promotion Reopen

Seal: GPU Timestamp Dispatch Slice Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4B` consumes the G211C3R4A timestamp query probe outputs as its entry authority and preserves the G211C3 `STOP_PERF_LOSS` result.

`70K-G211C3R4B` may only pass when G211C3R4A PASS is present, the G211C3R4A next entry packet to G211C3R4B is present, `timestamp_query_status = TIMESTAMP_QUERY_AVAILABLE`, `fallback_timing_policy = USE_GPU_TIMESTAMP_QUERY`, the G211C3 original shape benchmark matrix is present, all required shapes B0-B5 are measured, the G211C3 promotion stop is retained, and no G211C4 entry packet exists.

`70K-G211C3R4B` must not mutate the TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not implement TensorCube kernel optimization, must not rerun promotion, and must not claim TensorCore usage, speedup, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R4A
Timestamp Query Probe /
GPU Timing Feature Detection To Measurement Hygiene Repair /
No Runtime Splice No Promotion Reopen
```

Required predecessor evidence:

```text
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_TIMESTAMP_QUERY_PROBE.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_ADAPTER_FEATURE_FINGERPRINT.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_TIMESTAMP_SMOKE_RESULT.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_FALLBACK_TIMING_POLICY.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_NEXT_ENTRY_PACKET_G211C3R4B.json
artifacts/g211c3r4a/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4A.txt
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
```

## Purpose

G211C3R4B measures baseline and TensorCube candidate dispatch-only GPU elapsed time using timestamp query and separates it from dispatch plus readback CPU wall-clock timing.

G211C3R4B proves only this:

```text
G211C3 STOP_PERF_LOSS was preserved
G211C3R4A timestamp query availability was accepted as entry authority
baseline dispatch-only timestamp timing was measured for B0-B5
candidate dispatch-only timestamp timing was measured for B0-B5
dispatch plus readback wall-clock timing was recorded for pollution comparison
parity remained pass
runtime splice and promotion remained closed
```

G211C3R4B does not optimize TensorCube. G211C3R4B does not rerun benchmark promotion. G211C3R4B does not authorize G211C4.

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

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4b_dispatch_only_timing_probe.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4b_dispatch_only_timing_probe
```

Alternative command from `crates/base_train`:

```powershell
cargo run --bin ash_basetrain_gpu_70k_g211c3r4b_dispatch_only_timing_probe
```

Optional arguments:

```text
--g211c3-dir artifacts/g211c3
--g211c3r2-dir artifacts/g211c3r2
--g211c3r3-dir artifacts/g211c3r3
--g211c3r4a-dir artifacts/g211c3r4a
--out-dir artifacts/g211c3r4b
--warmup-iterations 20
--measured-iterations 100
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4B_DISPATCH_ONLY_TIMING_PROBE
```

## Timing Contract

G211C3R4B records timestamp query values for both baseline and candidate paths:

```text
timestamp_query_used=true
timestamp_start_raw
timestamp_end_raw
timestamp_delta_raw
timestamp_period_source
timestamp_delta_ns
timestamp_delta_ms
timestamp_delta_valid
```

Dispatch-only timing must not include:

```text
map_async wait
readback decode
CPU reference matmul
parity compare
JSON writing
pipeline creation
bind group layout creation
adapter request
device request
```

G211C3R4B also records dispatch plus readback wall-clock timing for diagnostic comparison only. This value must not override dispatch-only GPU timestamp timing.

## Probe Verdict Values

G211C3R4B must produce exactly one dispatch timing verdict.

```text
DISPATCH_ONLY_TIMING_CAPTURED
DISPATCH_ONLY_RAW_TIMESTAMP_CAPTURED
DISPATCH_ONLY_TIMESTAMP_UNSTABLE
DISPATCH_ONLY_TIMESTAMP_FAILED
DISPATCH_ONLY_PARITY_FAILED
DISPATCH_ONLY_MATRIX_INCOMPLETE
INCONCLUSIVE
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r4b` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_DISPATCH_ONLY_TIMING_PROBE.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_DISPATCH_ONLY_TIMING_MATRIX.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_READBACK_POLLUTION_SPLIT.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_NEXT_ENTRY_PACKET_G211C3R4C.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_BAKE_MANIFEST.json
artifacts/g211c3r4b/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4B.txt
```

Forbidden output:

```text
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_NEXT_ENTRY_PACKET_G211C4.json
```

## Main Receipt Required Fields

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-70K-G211C3R4B",
  "patch_name": "Dispatch Only Timing Probe",
  "status": "PASS_ASH_BASETRAIN_GPU_70K_G211C3R4B_DISPATCH_ONLY_TIMING_PROBE",
  "predecessor": "ASH-BASETRAIN-GPU-70K-G211C3R4A",
  "g211c3r4a_entry_verified": true,
  "g211c3_microbench_verdict": "STOP_PERF_LOSS",
  "g211c3r2_hygiene_verdict": "MEASUREMENT_HYGIENE_INCOMPLETE",
  "timestamp_query_status": "TIMESTAMP_QUERY_AVAILABLE",
  "fallback_timing_policy": "USE_GPU_TIMESTAMP_QUERY",
  "dispatch_timing_verdict": "DISPATCH_ONLY_TIMING_CAPTURED",
  "promotion_stop_retained": true,
  "runtime_splice_allowed": false,
  "promotion_allowed": false,
  "g211c4_entry_generated": false
}
```

## Next Gate

G211C3R4B routes to G211C3R4C, not G211C4.

```text
ASH-BASETRAIN-GPU-70K-G211C3R4C
Repeated Dispatch Batch Timing Crosscheck /
Small Shape Amortization Probe /
No Runtime Splice No Promotion Reopen
```

## PASS Criteria

```text
PASS-01 G211C3R4A PASS marker found
PASS-02 G211C3R4A next entry packet found
PASS-03 timestamp_query_status = TIMESTAMP_QUERY_AVAILABLE
PASS-04 fallback_timing_policy = USE_GPU_TIMESTAMP_QUERY
PASS-05 G211C3 STOP_PERF_LOSS retained
PASS-06 G211C4 entry packet absent
PASS-07 all required shapes B0-B5 present
PASS-08 baseline dispatch-only timestamp timing recorded
PASS-09 candidate dispatch-only timestamp timing recorded
PASS-10 dispatch plus readback timing recorded for comparison
PASS-11 timestamp stability audit written
PASS-12 readback pollution split written
PASS-13 parity remains pass
PASS-14 dispatch timing verdict selected exactly once
PASS-15 timing matrix written
PASS-16 promotion stop retained
PASS-17 runtime_splice_allowed=false
PASS-18 promotion_allowed=false
PASS-19 G211C3R4C entry packet generated
PASS-20 G211C4 entry packet not generated
PASS-21 forbidden mutation seal passed
PASS-22 PASS marker printed
```

## BLOCKED Codes

```text
ERR_70K_G211C3R4B_G211C3R4A_PASS_MARKER_MISSING
ERR_70K_G211C3R4B_G211C3R4A_ENTRY_PACKET_MISSING
ERR_70K_G211C3R4B_TIMESTAMP_NOT_AVAILABLE
ERR_70K_G211C3R4B_G211C3_MATRIX_MISSING
ERR_70K_G211C3R4B_REQUIRED_SHAPE_MISSING
ERR_70K_G211C3R4B_TIMESTAMP_DELTA_INVALID
ERR_70K_G211C3R4B_PARITY_FAILED
ERR_70K_G211C3R4B_UNEXPECTED_G211C4_ENTRY_PACKET
ERR_70K_G211C3R4B_RUNTIME_MUTATION_DETECTED
```

## PASS Meaning

PASS means G211C3R4B captured or explicitly audited dispatch-only GPU timestamp timing for required TensorCube microbench shapes while preserving the G211C3 STOP_PERF_LOSS state.

PASS does not mean TensorCube is faster. PASS does not mean TensorCube timing hygiene is fully repaired. PASS does not mean TensorCube optimization has been applied. PASS does not mean TensorCube promotion is reopened. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean production acceleration exists. PASS does not mean TensorCore is used.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4B dispatch only timing probe

- Add GPU timestamp dispatch-only timing probe gate
- Require G211C3R4A timestamp query availability as entry authority
- Measure baseline and TensorCube candidate dispatch-only timing for B0-B5
- Record dispatch plus readback timing for pollution comparison
- Add timestamp stability audit and readback pollution split
- Preserve G211C3 STOP_PERF_LOSS and promotion stop
- Route to G211C3R4C repeated dispatch batch timing crosscheck
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
