# ASH-BASETRAIN-GPU-70K-G211C3R4L-R1

## 8x8x4 Kernel Utilization Audit / Measured Route Kernel Identity Proof / No Runtime Splice No Promotion Reopen

Seal: Kernel Utilization Audit Only / Measured Route Kernel Identity Proof Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4L-R1` consumes the G211C3R4L fresh clean speedup probe outputs as its primary input authority. It preserves the R4L speedup verdict and does not recompute or rewrite R4L measurement artifacts.

R4L established clean timing execution, parity pass, timestamp stability, and `speedup_verdict = FRESH_CLEAN_SPEEDUP_NOT_RECOVERED`. R4L did not by itself prove that the intended 8x8x4 TensorCube kernel was actually the measured candidate route.

`70K-G211C3R4L-R1` may only pass when R4L PASS is present, `speedup_verdict = FRESH_CLEAN_SPEEDUP_NOT_RECOVERED`, `speedup_class = CLEAN_SPEEDUP_NOT_RECOVERED_NO_PROMOTION`, `primary_timing_authority = READBACK_FREE_DISPATCH_TIMESTAMP`, `correctness_authority = SINGLE_FINAL_MAP_PARITY_CHECK`, `required_probe_shape_count = 3`, `required_probe_shapes = B0,B1,B5`, `all_required_probe_shapes_measured = true`, `parity_pass = true`, `timestamp_stable = true`, `clean_speedup_recovered = false`, `runtime_splice_allowed = false`, `promotion_allowed = false`, and `g211c4_entry_generated = false`.

`70K-G211C3R4L-R1` must not rerun the fresh probe, must not rerun benchmark, must not recompute speedup ratio, must not rewrite R4L artifacts, must not mutate TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not optimize the TensorCube kernel, must not rewrite production WGSL, must not change production tile/workgroup/padding policy, must not rerun promotion, and must not claim TensorCore usage, speedup recovery, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R4L
Fresh Clean Speedup Probe Execution /
Readback-Free Dispatch Timing /
No Runtime Splice No Promotion Reopen
```

Required predecessor evidence:

```text
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_FRESH_CLEAN_SPEEDUP_PROBE_EXECUTION.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_FRESH_CLEAN_SPEEDUP_MATRIX.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_SINGLE_FINAL_MAP_PARITY_AUDIT.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_READBACK_FREE_DISPATCH_TIMING_AUDIT.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_CONTAMINATION_GUARD_EXECUTION_AUDIT.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_ROUTE_POLICY_REVIEW_INPUT.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_NEXT_ENTRY_PACKET_G211C3R4M.json
artifacts/g211c3r4l/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4L.txt
```

Forbidden output:

```text
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_NEXT_ENTRY_PACKET_G211C4.json
```

## Purpose

G211C3R4L-R1 audits whether the measured R4L candidate route actually utilized the intended 8x8x4 TensorCube kernel. It separates these statements:

```text
R4L measured route did not recover speedup.
The intended 8x8x4 kernel did not recover speedup.
The intended 8x8x4 kernel was not proven to be used.
The measured route may have been fallback/scalar/reference contaminated.
```

R4L-R1 proves only kernel utilization attribution. It does not prove speedup, promotion, runtime splice, or G211C4 readiness.

## Kernel Identity Evidence Model

R4L-R1 checks these evidence layers:

```text
planned_kernel_identity
pipeline_label_identity
shader_or_workgroup_identity
dispatch_route_identity
runtime_kernel_hit_count
timestamp_envelope_identity
fallback_absence
per_shape_coverage_B0_B1_B5
```

Required runtime evidence fields, when available:

```text
kernel_identity
pipeline_identity
dispatch_identity
tile_shape
workgroup_shape
microtile_shape
kernel_hit_count
fallback_route_used
reference_route_used
scalar_route_used
timestamp_envelope_target
```

Expected values:

```text
kernel_identity = TENSORCUBE_8X8X4
pipeline_identity contains 8x8x4 or tensorcube_8x8x4
dispatch_identity contains 8x8x4 or tensorcube_8x8x4
tile_shape = [8,8,4]
microtile_shape = [8,8,4]
fallback_route_used = false
reference_route_used = false
scalar_route_used = false
timestamp_envelope_target = TENSORCUBE_8X8X4_DISPATCH
```

Per-shape requirement for full confirmation:

```text
B0 kernel_hit_count >= 1
B1 kernel_hit_count >= 1
B5 kernel_hit_count >= 1
```

If runtime receipts do not expose these fields, R4L-R1 must report `KERNEL_8X8X4_UTILIZATION_UNPROVEN`. It must not fabricate hits from source labels.

## Utilization Verdict Values

```text
KERNEL_8X8X4_UTILIZATION_CONFIRMED
KERNEL_8X8X4_UTILIZATION_PARTIAL
KERNEL_8X8X4_UTILIZATION_UNPROVEN
KERNEL_8X8X4_NOT_USED
MEASURED_ROUTE_IDENTITY_CONTRADICTION
FALLBACK_ROUTE_CONTAMINATION_DETECTED
TIMESTAMP_ENVELOPE_MISMATCH
UTILIZATION_AUDIT_INCOMPLETE
INCONCLUSIVE
```

Decision mapping:

```text
KERNEL_8X8X4_UTILIZATION_CONFIRMED -> SPEEDUP_FAILURE_ATTRIBUTABLE_TO_8X8X4
KERNEL_8X8X4_UTILIZATION_PARTIAL -> SPEEDUP_FAILURE_PARTIAL_KERNEL_COVERAGE
KERNEL_8X8X4_UTILIZATION_UNPROVEN -> SPEEDUP_FAILURE_ROUTE_BINDING_UNPROVEN
KERNEL_8X8X4_NOT_USED -> SPEEDUP_FAILURE_ROUTE_BINDING_FAILURE
FALLBACK_ROUTE_CONTAMINATION_DETECTED -> SPEEDUP_FAILURE_FALLBACK_CONTAMINATED
TIMESTAMP_ENVELOPE_MISMATCH -> SPEEDUP_FAILURE_TIMESTAMP_ENVELOPE_INVALID
```

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4l_r1_kernel_utilization_audit.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4l_r1_kernel_utilization_audit
```

Optional args:

```text
--g211c3r4k-dir artifacts/g211c3r4k
--g211c3r4l-dir artifacts/g211c3r4l
--source-root .
--out-dir artifacts/g211c3r4l_r1
--expected-kernel TENSORCUBE_8X8X4
--expected-tile 8,8,4
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_KERNEL_UTILIZATION_AUDIT
```

Expected stdout fields:

```text
patch_id=ASH-BASETRAIN-GPU-70K-G211C3R4L-R1
kernel_utilization_verdict=<...>
speedup_reinterpretation_class=<...>
r4l_speedup_verdict_preserved=FRESH_CLEAN_SPEEDUP_NOT_RECOVERED
r4l_speedup_recomputed=false
r4l_artifacts_rewritten=false
expected_kernel_identity=TENSORCUBE_8X8X4
required_probe_shape_count=3
required_probe_shapes=B0,B1,B5
all_required_shape_kernel_hits_confirmed=<true|false>
fallback_route_contamination_detected=<true|false>
timestamp_envelope_matches_kernel=<true|false>
speedup_failure_attributable_to_8x8x4=<true|false>
route_binding_failure_possible=<true|false>
operator_review_required=true
runtime_splice_allowed=false
promotion_allowed=false
g211c4_entry_generated=false
next_gate=ASH-BASETRAIN-GPU-70K-G211C3R4L-R2
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r4l_r1` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_KERNEL_UTILIZATION_AUDIT.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_MEASURED_ROUTE_KERNEL_IDENTITY_PROOF.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_PIPELINE_BIND_AUDIT.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_DISPATCH_HIT_LEDGER.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_FALLBACK_ABSENCE_AUDIT.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_TIMESTAMP_ENVELOPE_AUDIT.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_R4L_SPEEDUP_REINTERPRETATION.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_NEXT_ENTRY_PACKET_G211C3R4L_R2.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_BAKE_MANIFEST.json
artifacts/g211c3r4l_r1/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4L_R1.txt
```

## PASS Criteria

```text
PASS-01 R4L PASS marker found
PASS-02 R4L speedup_verdict = FRESH_CLEAN_SPEEDUP_NOT_RECOVERED
PASS-03 R4L speedup_class = CLEAN_SPEEDUP_NOT_RECOVERED_NO_PROMOTION
PASS-04 R4L primary_timing_authority = READBACK_FREE_DISPATCH_TIMESTAMP
PASS-05 R4L correctness_authority = SINGLE_FINAL_MAP_PARITY_CHECK
PASS-06 R4L required_probe_shape_count = 3
PASS-07 R4L required_probe_shapes = B0,B1,B5
PASS-08 R4L all_required_probe_shapes_measured=true
PASS-09 R4L parity_pass=true
PASS-10 R4L timestamp_stable=true
PASS-11 R4L clean_speedup_recovered=false
PASS-12 kernel utilization audit written
PASS-13 measured route kernel identity proof written
PASS-14 pipeline bind audit written
PASS-15 dispatch hit ledger written
PASS-16 fallback absence audit written
PASS-17 timestamp envelope audit written
PASS-18 R4L speedup reinterpretation written
PASS-19 R4L speedup verdict preserved
PASS-20 R4L speedup not recomputed
PASS-21 R4L artifacts not rewritten
PASS-22 utilization verdict selected exactly once
PASS-23 reinterpretation class selected exactly once
PASS-24 promotion stop retained
PASS-25 runtime_splice_allowed=false
PASS-26 promotion_allowed=false
PASS-27 G211C3R4L-R2 entry packet generated
PASS-28 G211C4 entry packet not generated
PASS-29 forbidden mutation seal passed
PASS-30 PASS marker printed
```

## PASS Meaning

PASS means R4L-R1 audited whether the R4L measured route actually utilized the intended 8x8x4 TensorCube kernel and reinterpreted the R4L speedup failure accordingly.

PASS does not mean 8x8x4 was used unless `kernel_utilization_verdict = KERNEL_8X8X4_UTILIZATION_CONFIRMED`.

PASS does not mean 8x8x4 is slow unless `speedup_reinterpretation_class = SPEEDUP_FAILURE_ATTRIBUTABLE_TO_8X8X4`.

PASS does not mean speedup recovered. PASS does not mean promotion is allowed. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean production acceleration exists. PASS does not mean TensorCore is used.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4L-R1 kernel utilization audit

- Add 8x8x4 kernel utilization audit gate
- Require R4L fresh clean speedup probe as entry authority
- Verify measured route kernel identity and dispatch hit evidence
- Audit pipeline bind, fallback absence, and timestamp envelope
- Preserve R4L speedup verdict without recomputation
- Reinterpret speedup failure only after kernel utilization proof
- Route to G211C3R4L-R2 without G211C4 entry
- Preserve no runtime splice, no production route, no promotion
```
