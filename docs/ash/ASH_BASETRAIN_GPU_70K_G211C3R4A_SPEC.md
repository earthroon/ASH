# ASH-BASETRAIN-GPU-70K-G211C3R4A

## Timestamp Query Probe / GPU Timing Feature Detection To Measurement Hygiene Repair / No Runtime Splice No Promotion Reopen

Seal: Timestamp Feature Detection Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4A` consumes the G211C3R3 optimization candidate plan outputs as its entry authority and preserves the G211C3 `STOP_PERF_LOSS` result.

`70K-G211C3R4A` may only pass when G211C3R3 PASS is present, the G211C3R3 next entry packet to G211C3R4 is present, the G211C3R3 patch queue is present, `first_patch_key = G211C3R4A_TIMESTAMP_QUERY_PROBE`, the G211C3 promotion stop is retained, and no G211C4 entry packet exists.

`70K-G211C3R4A` must not mutate the TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not implement TensorCube kernel optimization, must not rerun promotion, and must not claim TensorCore usage, speedup, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R3
TensorCube Targeted Optimization Candidate Plan /
Overhead Verdict To Patch Queue /
No Runtime Splice No Promotion Reopen
```

Required predecessor evidence:

```text
artifacts/g211c3r3/ASH_BASETRAIN_GPU_70K_G211C3R3_OPTIMIZATION_CANDIDATE_PLAN.json
artifacts/g211c3r3/ASH_BASETRAIN_GPU_70K_G211C3R3_PATCH_QUEUE.json
artifacts/g211c3r3/ASH_BASETRAIN_GPU_70K_G211C3R3_PRIORITY_DECISION_TRACE.json
artifacts/g211c3r3/ASH_BASETRAIN_GPU_70K_G211C3R3_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r3/ASH_BASETRAIN_GPU_70K_G211C3R3_NEXT_ENTRY_PACKET_G211C3R4.json
artifacts/g211c3r3/PASS_ASH_BASETRAIN_GPU_70K_G211C3R3.txt
```

Optional context evidence:

```text
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_OVERHEAD_ISOLATION.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_MEASUREMENT_HYGIENE_AUDIT.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_TIMING_COMPONENT_MATRIX.json
```

Forbidden evidence:

```text
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r3/ASH_BASETRAIN_GPU_70K_G211C3R3_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_NEXT_ENTRY_PACKET_G211C4.json
```

## Purpose

G211C3R4A probes whether the current WGPU adapter/device/backend can provide GPU timestamp query timing for later dispatch-only microbench hygiene.

G211C3R4A proves only this:

```text
G211C3 STOP_PERF_LOSS was preserved
G211C3R3 patch queue was accepted as entry authority
first_patch_key = G211C3R4A_TIMESTAMP_QUERY_PROBE was verified
adapter feature fingerprint was recorded
timestamp query availability was detected or explicitly ruled out
timestamp smoke result was recorded or explicitly unavailable
fallback timing policy was selected
runtime splice and promotion remained closed
```

G211C3R4A does not optimize TensorCube. G211C3R4A does not rerun benchmark promotion. G211C3R4A does not authorize G211C4.

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4a_timestamp_query_probe.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4a_timestamp_query_probe
```

Alternative command from `crates/base_train`:

```powershell
cargo run --bin ash_basetrain_gpu_70k_g211c3r4a_timestamp_query_probe
```

Optional arguments:

```text
--g211c3-dir artifacts/g211c3
--g211c3r2-dir artifacts/g211c3r2
--g211c3r3-dir artifacts/g211c3r3
--out-dir artifacts/g211c3r4a
--attempt-smoke true
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4A_TIMESTAMP_QUERY_PROBE
```

## Timestamp Status Values

G211C3R4A must produce exactly one timestamp status.

```text
TIMESTAMP_QUERY_AVAILABLE
FEATURE_ABSENT
FEATURE_PRESENT_DEVICE_REQUEST_FAILED
QUERY_SET_CREATE_FAILED
TIMESTAMP_WRITE_UNAVAILABLE
TIMESTAMP_RESOLVE_FAILED
TIMESTAMP_READBACK_FAILED
TIMESTAMP_DELTA_INVALID
BACKEND_UNSUPPORTED
API_VERSION_UNRESOLVED
INCONCLUSIVE
```

`TIMESTAMP_QUERY_AVAILABLE` is allowed only when the timestamp query feature is visible, device request grants it, query set creation succeeds, timestamp writes resolve, readback succeeds, and the raw delta is valid.

If the adapter does not expose timestamp query support, status must be `FEATURE_ABSENT`.

If project-local WGPU API naming prevents safe implementation without a version-specific fix, status must be `API_VERSION_UNRESOLVED`.

Do not fake timestamp values.

## Fallback Timing Policy

G211C3R4A must select exactly one fallback timing policy.

```text
USE_GPU_TIMESTAMP_QUERY
USE_BATCH_AMORTIZED_CPU_WALL_CLOCK
USE_CPU_WALL_CLOCK_DISPATCH_READBACK_SPLIT
USE_EXISTING_C3_TIMING_ONLY
TIMING_POLICY_BLOCKED
```

Selection rules:

```text
TIMESTAMP_QUERY_AVAILABLE -> USE_GPU_TIMESTAMP_QUERY
FEATURE_ABSENT -> USE_BATCH_AMORTIZED_CPU_WALL_CLOCK
FEATURE_PRESENT_DEVICE_REQUEST_FAILED -> USE_BATCH_AMORTIZED_CPU_WALL_CLOCK
QUERY_SET_CREATE_FAILED -> USE_BATCH_AMORTIZED_CPU_WALL_CLOCK
TIMESTAMP_WRITE_UNAVAILABLE -> USE_BATCH_AMORTIZED_CPU_WALL_CLOCK
TIMESTAMP_RESOLVE_FAILED -> USE_BATCH_AMORTIZED_CPU_WALL_CLOCK
TIMESTAMP_READBACK_FAILED -> USE_BATCH_AMORTIZED_CPU_WALL_CLOCK
TIMESTAMP_DELTA_INVALID -> USE_BATCH_AMORTIZED_CPU_WALL_CLOCK
BACKEND_UNSUPPORTED -> USE_BATCH_AMORTIZED_CPU_WALL_CLOCK
API_VERSION_UNRESOLVED -> USE_BATCH_AMORTIZED_CPU_WALL_CLOCK
INCONCLUSIVE -> USE_CPU_WALL_CLOCK_DISPATCH_READBACK_SPLIT
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r4a` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_TIMESTAMP_QUERY_PROBE.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_ADAPTER_FEATURE_FINGERPRINT.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_TIMESTAMP_SMOKE_RESULT.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_FALLBACK_TIMING_POLICY.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_NEXT_ENTRY_PACKET_G211C3R4B.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_BAKE_MANIFEST.json
artifacts/g211c3r4a/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4A.txt
```

Forbidden output:

```text
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_NEXT_ENTRY_PACKET_G211C4.json
```

## Main Receipt Required Fields

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-70K-G211C3R4A",
  "patch_name": "Timestamp Query Probe",
  "status": "PASS_ASH_BASETRAIN_GPU_70K_G211C3R4A_TIMESTAMP_QUERY_PROBE",
  "predecessor": "ASH-BASETRAIN-GPU-70K-G211C3R3",
  "g211c3r3_entry_verified": true,
  "g211c3_microbench_verdict": "STOP_PERF_LOSS",
  "g211c3r2_hygiene_verdict": "MEASUREMENT_HYGIENE_INCOMPLETE",
  "plan_verdict": "PLAN_MEASUREMENT_HYGIENE_REPAIR",
  "first_patch_key_verified": "G211C3R4A_TIMESTAMP_QUERY_PROBE",
  "promotion_stop_retained": true,
  "runtime_splice_allowed": false,
  "promotion_allowed": false,
  "g211c4_entry_generated": false,
  "timestamp_probe": {
    "timestamp_query_status": "FEATURE_ABSENT",
    "timestamp_query_feature_visible": false,
    "timestamp_feature_requested": false,
    "timestamp_feature_granted": false,
    "query_set_create_attempted": false,
    "query_set_create_succeeded": false,
    "timestamp_write_attempted": false,
    "timestamp_write_succeeded": false,
    "timestamp_resolve_attempted": false,
    "timestamp_resolve_succeeded": false,
    "timestamp_readback_attempted": false,
    "timestamp_readback_succeeded": false,
    "timestamp_delta_valid": false,
    "timestamp_delta_raw": null,
    "timestamp_delta_ns": null
  },
  "fallback": {
    "fallback_timing_policy": "USE_BATCH_AMORTIZED_CPU_WALL_CLOCK",
    "c3r4b_dispatch_only_probe_allowed": true,
    "c3r4b_timestamp_mode_allowed": false,
    "c3r4b_batch_amortization_required": true
  }
}
```

## Adapter Feature Fingerprint

The adapter feature fingerprint must record:

```text
adapter.name
adapter.vendor
adapter.device
adapter.device_type
adapter.backend
adapter.driver
adapter.driver_info
features.raw_features_debug
features.timestamp_query_feature_visible
features.timestamp_feature_symbol_used
features.timestamp_query_inside_pass_supported
limits.max_buffer_size
limits.max_storage_buffer_binding_size
device_request.requested_timestamp_feature
device_request.granted_timestamp_feature
device_request.request_error
```

## Timestamp Smoke Result

The timestamp smoke result must record:

```text
smoke_attempted
smoke_succeeded
smoke_mode
query_count
timestamp_write_path
resolve_path
readback_path
timestamp_delta_raw
timestamp_delta_ns
timestamp_delta_valid
failure_reason
```

The smoke pass must not touch model weights, decode output, TensorCube production route, training state, checkpoints, or optimizer state.

## Next Gate

G211C3R4A routes to G211C3R4B, not G211C4.

```text
ASH-BASETRAIN-GPU-70K-G211C3R4B
Dispatch Only Timing Probe /
Timestamp Or Batch-Amortized Timing Split /
No Runtime Splice No Promotion Reopen
```

## PASS Criteria

```text
PASS-01 G211C3R3 PASS marker found
PASS-02 G211C3R3 next entry packet found
PASS-03 first_patch_key = G211C3R4A_TIMESTAMP_QUERY_PROBE
PASS-04 G211C3 STOP_PERF_LOSS retained
PASS-05 G211C4 entry packet absent
PASS-06 adapter fingerprint recorded
PASS-07 timestamp query feature visibility recorded
PASS-08 device request result recorded
PASS-09 query set creation result recorded when applicable
PASS-10 timestamp smoke result recorded or explicitly unavailable
PASS-11 timestamp status selected exactly once
PASS-12 fallback timing policy selected exactly once
PASS-13 G211C3R4B entry packet generated
PASS-14 G211C4 entry packet not generated
PASS-15 runtime_splice_allowed=false
PASS-16 promotion_allowed=false
PASS-17 forbidden mutation seal passed
PASS-18 PASS marker printed
```

## BLOCKED Codes

```text
ERR_70K_G211C3R4A_G211C3R3_PASS_MARKER_MISSING
ERR_70K_G211C3R4A_G211C3R3_ENTRY_PACKET_MISSING
ERR_70K_G211C3R4A_FIRST_PATCH_KEY_MISMATCH
ERR_70K_G211C3R4A_UNEXPECTED_G211C4_ENTRY_PACKET
ERR_70K_G211C3R4A_ADAPTER_REQUEST_FAILED
ERR_70K_G211C3R4A_DEVICE_REQUEST_FAILED_WITHOUT_RECEIPT
ERR_70K_G211C3R4A_RUNTIME_MUTATION_DETECTED
```

## PASS Meaning

PASS means G211C3R4A detected or explicitly ruled out GPU timestamp query availability and selected a timing policy for the next dispatch-only timing probe.

PASS does not mean TensorCube is faster. PASS does not mean TensorCube timing is now complete. PASS does not mean TensorCube optimization has been applied. PASS does not mean TensorCube promotion is reopened. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean production acceleration exists. PASS does not mean TensorCore is used.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4A timestamp query probe

- Add timestamp query probe gate
- Require G211C3R3 patch queue as entry authority
- Verify first patch key G211C3R4A_TIMESTAMP_QUERY_PROBE
- Record adapter feature fingerprint
- Detect timestamp query feature visibility and device request result
- Attempt timestamp smoke only when supported
- Select fallback timing policy without fabricating timing values
- Route to G211C3R4B dispatch-only timing probe
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
