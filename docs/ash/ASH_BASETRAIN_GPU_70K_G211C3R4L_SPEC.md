# ASH-BASETRAIN-GPU-70K-G211C3R4L

## Fresh Clean Speedup Probe Execution / Readback-Free Dispatch Timing / No Runtime Splice No Promotion Reopen

Seal: Fresh Clean Speedup Probe Execution Only / Readback-Free Dispatch Timing Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4L` consumes the G211C3R4K fresh clean speedup probe plan as its primary input authority and preserves the G211C3 `STOP_PERF_LOSS` result.

`70K-G211C3R4L` may only pass when R4K PASS is present, `probe_plan_verdict = FRESH_CLEAN_SPEEDUP_PROBE_PLAN_READY`, `probe_plan_class = FRESH_CLEAN_SPEEDUP_PROBE_PLAN_READY`, `primary_timing_authority = READBACK_FREE_DISPATCH_TIMESTAMP`, `correctness_authority = SINGLE_FINAL_MAP_PARITY_CHECK`, `required_probe_shape_count = 3`, `required_probe_shapes = B0,B1,B5`, `readback_free_timing_contract_ready = true`, `single_final_map_parity_plan_ready = true`, `contamination_guard_plan_ready = true`, `operator_review_packet_ready = true`, `route_policy_review_packet_ready = true`, `runtime_splice_allowed = false`, `promotion_allowed = false`, `g211c4_entry_generated = false`, and `next_gate = ASH-BASETRAIN-GPU-70K-G211C3R4L`.

`70K-G211C3R4L` must not mutate TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not implement TensorCube kernel optimization, must not rewrite a production WGSL kernel, must not change production tile/workgroup/padding policy, must not rerun promotion, and must not claim TensorCore usage, production readiness, or production acceleration. A clean speedup result is review evidence only, not promotion authority.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R4K
Fresh Clean Speedup Probe Plan /
Post Hygiene Measurement Route Review /
No Runtime Splice No Promotion Reopen
```

Required predecessor evidence:

```text
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_FRESH_CLEAN_SPEEDUP_PROBE_PLAN.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_TIMING_AUTHORITY_CONTRACT.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_PROBE_SHAPE_PLAN.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_CONTAMINATION_GUARD_PLAN.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_OPERATOR_REVIEW_PACKET.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_ROUTE_POLICY_REVIEW_PACKET.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_NEXT_ENTRY_PACKET_G211C3R4L.json
artifacts/g211c3r4k/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4K.txt
```

Forbidden output:

```text
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_NEXT_ENTRY_PACKET_G211C4.json
```

## Purpose

G211C3R4L executes the fresh clean speedup probe planned by G211C3R4K. It measures B0/B1/B5 under readback-free dispatch timestamp authority, verifies correctness with single-final-map parity, and emits a speedup verdict for operator review.

G211C3R4L proves only this:

```text
R4K fresh probe plan is valid
B0/B1/B5 fresh clean speedup probe executed
READBACK_FREE_DISPATCH_TIMESTAMP is the primary timing authority
SINGLE_FINAL_MAP_PARITY_CHECK is the correctness authority
per-iteration output map was excluded from measured interval
artifact write was excluded from measured interval
speedup verdict was produced for review
operator review is required
runtime splice remains blocked
promotion remains blocked
G211C4 remains blocked
```

## Timing and Correctness Contract

```text
primary_timing_authority = READBACK_FREE_DISPATCH_TIMESTAMP
correctness_authority = SINGLE_FINAL_MAP_PARITY_CHECK
secondary_wall_timing = not primary authority
per_iteration_output_map = forbidden
artifact_write_inside_measured_interval = forbidden
```

Implementation rule:

```text
Measured iterations may resolve timestamp readback, but output readback for parity must be performed as a single final map outside the measured timing interval.
```

## Required Probe Shapes

```text
B0 = [8, 8, 8]
B1 = [16, 16, 8]
B5 = [17, 31, 65]
```

B0/B1/B5 are mandatory. R4L must fail if any required shape is missing.

## Speedup Verdict Values

```text
FRESH_CLEAN_SPEEDUP_RECOVERED
FRESH_CLEAN_SPEEDUP_NEUTRAL
FRESH_CLEAN_SPEEDUP_NOT_RECOVERED
FRESH_CLEAN_SPEEDUP_PARITY_FAILED
FRESH_CLEAN_SPEEDUP_TIMESTAMP_UNSTABLE
FRESH_CLEAN_SPEEDUP_INCONCLUSIVE
```

Recommended policy:

```text
FRESH_CLEAN_SPEEDUP_RECOVERED:
  geomean_clean_speedup_ratio >= 1.02
  min_clean_speedup_ratio >= 1.00
  parity_pass = true
  timestamp_stable = true

FRESH_CLEAN_SPEEDUP_NEUTRAL:
  geomean_clean_speedup_ratio >= 1.00
  min_clean_speedup_ratio >= 0.98
  parity_pass = true
  timestamp_stable = true

FRESH_CLEAN_SPEEDUP_NOT_RECOVERED:
  otherwise, if parity_pass = true and timestamp_stable = true
```

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4l_fresh_clean_speedup_probe_execution.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4l_fresh_clean_speedup_probe_execution
```

Optional args:

```text
--g211c3-dir artifacts/g211c3
--g211c3r4k-dir artifacts/g211c3r4k
--out-dir artifacts/g211c3r4l
--probe-shapes B0,B1,B5
--warmup-iterations 20
--measured-iterations 100
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4L_FRESH_CLEAN_SPEEDUP_PROBE_EXECUTION
```

Expected stdout fields:

```text
patch_id=ASH-BASETRAIN-GPU-70K-G211C3R4L
speedup_verdict=<...>
speedup_class=<...>
primary_timing_authority=READBACK_FREE_DISPATCH_TIMESTAMP
correctness_authority=SINGLE_FINAL_MAP_PARITY_CHECK
required_probe_shape_count=3
required_probe_shapes=B0,B1,B5
geomean_clean_speedup_ratio=<f64>
min_clean_speedup_ratio=<f64>
all_required_probe_shapes_measured=true
parity_pass=true
timestamp_stable=true
clean_speedup_recovered=<true|false>
operator_review_required=true
runtime_splice_allowed=false
promotion_allowed=false
g211c4_entry_generated=false
next_gate=ASH-BASETRAIN-GPU-70K-G211C3R4M
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r4l` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_FRESH_CLEAN_SPEEDUP_PROBE_EXECUTION.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_FRESH_CLEAN_SPEEDUP_MATRIX.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_SINGLE_FINAL_MAP_PARITY_AUDIT.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_READBACK_FREE_DISPATCH_TIMING_AUDIT.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_CONTAMINATION_GUARD_EXECUTION_AUDIT.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_ROUTE_POLICY_REVIEW_INPUT.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_NEXT_ENTRY_PACKET_G211C3R4M.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r4l/ASH_BASETRAIN_GPU_70K_G211C3R4L_BAKE_MANIFEST.json
artifacts/g211c3r4l/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4L.txt
```

## PASS Meaning

PASS means G211C3R4L executed the fresh clean speedup probe under the R4K timing contract, produced clean dispatch timing evidence for B0/B1/B5, verified single-final-map parity, and routed to R4M for operator review without runtime splice, promotion reopen, or G211C4 entry.

PASS does not mean promotion is allowed. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean TensorCore is used. PASS does not mean speedup evidence can be applied without operator review.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4L fresh clean speedup probe execution

- Add fresh clean speedup probe execution gate
- Require R4K fresh probe plan as entry authority
- Run B0/B1/B5 under readback-free dispatch timestamp authority
- Use single-final-map parity as correctness authority
- Exclude per-iteration output map and artifact write from measured interval
- Emit clean speedup verdict and matrix
- Route to G211C3R4M operator review
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
