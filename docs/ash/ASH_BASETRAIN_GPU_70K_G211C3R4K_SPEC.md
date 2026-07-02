# ASH-BASETRAIN-GPU-70K-G211C3R4K

## Fresh Clean Speedup Probe Plan / Post Hygiene Measurement Route Review / No Runtime Splice No Promotion Reopen

Seal: Fresh Clean Speedup Probe Plan Only / Post Hygiene Measurement Route Review Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4K` consumes the G211C3R4J measurement hygiene closeout outputs as its primary input authority and preserves the G211C3 `STOP_PERF_LOSS` result.

`70K-G211C3R4K` may only pass when R4J PASS is present, `closeout_verdict = MEASUREMENT_HYGIENE_CLOSEOUT_COMPLETE`, `closeout_class = MEASUREMENT_HYGIENE_CLOSED`, `r4e_mixed_loss_final_state = REJECTED`, `poll_map_contamination_lineage_closed = true`, `b5_clean_residual_low_sealed = true`, `c3_stop_perf_loss_retained = true`, `promotion_stop_retained = true`, `route_policy_review_required = true`, `fresh_clean_speedup_probe_recommended = true`, `runtime_splice_allowed = false`, `promotion_allowed = false`, `g211c4_entry_generated = false`, and `next_gate = ASH-BASETRAIN-GPU-70K-G211C3R4K`.

`70K-G211C3R4K` must not run the fresh probe, must not mutate TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not implement TensorCube kernel optimization, must not rewrite a production WGSL kernel, must not change production tile/workgroup/padding policy, must not rerun promotion, and must not claim TensorCore usage, speedup, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R4J
Measurement Hygiene Closeout /
Route Policy Review Recommendation /
No Runtime Splice No Promotion Reopen
```

Required predecessor evidence:

```text
artifacts/g211c3r4j/ASH_BASETRAIN_GPU_70K_G211C3R4J_MEASUREMENT_HYGIENE_CLOSEOUT.json
artifacts/g211c3r4j/ASH_BASETRAIN_GPU_70K_G211C3R4J_R4E_REJECTION_CLOSEOUT.json
artifacts/g211c3r4j/ASH_BASETRAIN_GPU_70K_G211C3R4J_CONTAMINATION_LINEAGE_CLOSEOUT.json
artifacts/g211c3r4j/ASH_BASETRAIN_GPU_70K_G211C3R4J_ROUTE_POLICY_RECOMMENDATION.json
artifacts/g211c3r4j/ASH_BASETRAIN_GPU_70K_G211C3R4J_FRESH_CLEAN_SPEEDUP_PROBE_RECOMMENDATION.json
artifacts/g211c3r4j/ASH_BASETRAIN_GPU_70K_G211C3R4J_PROMOTION_STOP_RETENTION_SEAL.json
artifacts/g211c3r4j/ASH_BASETRAIN_GPU_70K_G211C3R4J_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4j/ASH_BASETRAIN_GPU_70K_G211C3R4J_NEXT_ENTRY_PACKET_G211C3R4K.json
artifacts/g211c3r4j/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4J.txt
```

Forbidden evidence includes any `NEXT_ENTRY_PACKET_G211C4` in the C3/R4 path, including:

```text
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_NEXT_ENTRY_PACKET_G211C4.json
```

## Purpose

G211C3R4K prepares the fresh clean speedup probe plan after measurement hygiene closeout. It defines clean timing authority, required probe shapes, contamination guards, operator review, and route policy review packets without reopening promotion.

G211C3R4K proves only this:

```text
R4J measurement hygiene closeout is complete
R4E mixed loss is rejected and not current authority
C3 STOP_PERF_LOSS remains active
fresh clean speedup probe is required before route reconsideration
fresh clean speedup probe is not a promotion gate
fresh clean speedup probe is not a runtime splice gate
fresh clean speedup probe may not generate G211C4 entry
readback-free dispatch timing is the primary timing authority
single-final-map parity check is mandatory
per-iteration map timing is forbidden in measured interval
artifact write is forbidden in measured interval
operator review is required after R4L probe result
```

## Timing Authority Contract

```text
primary_timing_authority = READBACK_FREE_DISPATCH_TIMESTAMP
secondary_wall_timing = QUEUE_SUBMIT_WALL_EXCLUDING_MAP_AND_ARTIFACT_WRITE
correctness_authority = SINGLE_FINAL_MAP_PARITY_CHECK
forbidden_timing_authority = PER_ITERATION_MAP_TOTAL_WALL
```

Required R4L paths:

```text
READBACK_FREE_DISPATCH_TIMESTAMP
SINGLE_FINAL_MAP_PARITY
NO_ARTIFACT_WRITE_MEASURED_INTERVAL
NO_PER_ITERATION_MAP
```

Forbidden timing paths:

```text
PER_ITERATION_MAP_AS_SPEEDUP_AUTHORITY
ARTIFACT_WRITE_INSIDE_MEASURED_INTERVAL
MAP_ASYNC_WAIT_INSIDE_DISPATCH_TIMING
POLL_WAIT_AS_KERNEL_ATTRIBUTION
READBACK_WALL_TOTAL_AS_PRIMARY_SPEEDUP_AUTHORITY
```

## Required Probe Shapes

```text
B0 = [8, 8, 8]
B1 = [16, 16, 8]
B5 = [17, 31, 65]
```

Optional context shapes:

```text
B2 = [16, 16, 64]
B5_PAD8 = [24, 32, 72]
B5_NEAR_EVEN = [16, 32, 64]
```

## Probe Plan Classes

```text
FRESH_CLEAN_SPEEDUP_PROBE_PLAN_READY
READBACK_FREE_TIMING_CONTRACT_READY
SINGLE_FINAL_MAP_PARITY_PLAN_READY
CONTAMINATION_GUARD_PLAN_READY
OPERATOR_REVIEW_PACKET_READY
PROBE_PLAN_INCOMPLETE
PROBE_PLAN_CONTRADICTION_DETECTED
PROBE_PLAN_FORBIDDEN_PROMOTION_REOPEN
PROBE_PLAN_FORBIDDEN_G211C4_ENTRY
INCONCLUSIVE
```

Preferred class:

```text
FRESH_CLEAN_SPEEDUP_PROBE_PLAN_READY
```

## Probe Plan Verdict Values

```text
FRESH_CLEAN_SPEEDUP_PROBE_PLAN_READY
POST_HYGIENE_ROUTE_REVIEW_READY
READBACK_FREE_TIMING_CONTRACT_READY
CONTAMINATION_GUARD_READY
OPERATOR_REVIEW_REQUIRED_AFTER_R4L
PROBE_PLAN_INCOMPLETE
PROBE_PLAN_CONTRADICTION_DETECTED
PROBE_PLAN_FORBIDDEN_PROMOTION_REOPEN
PROBE_PLAN_FORBIDDEN_G211C4_ENTRY
INCONCLUSIVE
```

Preferred safe verdict:

```text
FRESH_CLEAN_SPEEDUP_PROBE_PLAN_READY
```

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4k_fresh_clean_speedup_probe_plan.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4k_fresh_clean_speedup_probe_plan
```

Optional args:

```text
--g211c3-dir artifacts/g211c3
--g211c3r2-dir artifacts/g211c3r2
--g211c3r3-dir artifacts/g211c3r3
--g211c3r4a-dir artifacts/g211c3r4a
--g211c3r4b-dir artifacts/g211c3r4b
--g211c3r4c-dir artifacts/g211c3r4c
--g211c3r4d-dir artifacts/g211c3r4d
--g211c3r4d-r2-dir artifacts/g211c3r4d_r2
--g211c3r4e-dir artifacts/g211c3r4e
--g211c3r4f-dir artifacts/g211c3r4f
--g211c3r4g-dir artifacts/g211c3r4g
--g211c3r4h-dir artifacts/g211c3r4h
--g211c3r4i-dir artifacts/g211c3r4i
--g211c3r4j-dir artifacts/g211c3r4j
--out-dir artifacts/g211c3r4k
--probe-shapes B0,B1,B5
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4K_FRESH_CLEAN_SPEEDUP_PROBE_PLAN
```

Expected stdout fields:

```text
patch_id=ASH-BASETRAIN-GPU-70K-G211C3R4K
probe_plan_verdict=FRESH_CLEAN_SPEEDUP_PROBE_PLAN_READY
probe_plan_class=FRESH_CLEAN_SPEEDUP_PROBE_PLAN_READY
primary_timing_authority=READBACK_FREE_DISPATCH_TIMESTAMP
correctness_authority=SINGLE_FINAL_MAP_PARITY_CHECK
required_probe_shape_count=3
required_probe_shapes=B0,B1,B5
readback_free_timing_contract_ready=true
single_final_map_parity_plan_ready=true
contamination_guard_plan_ready=true
operator_review_packet_ready=true
route_policy_review_packet_ready=true
runtime_splice_allowed=false
promotion_allowed=false
g211c4_entry_generated=false
next_gate=ASH-BASETRAIN-GPU-70K-G211C3R4L
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r4k` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_FRESH_CLEAN_SPEEDUP_PROBE_PLAN.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_TIMING_AUTHORITY_CONTRACT.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_PROBE_SHAPE_PLAN.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_CONTAMINATION_GUARD_PLAN.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_OPERATOR_REVIEW_PACKET.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_ROUTE_POLICY_REVIEW_PACKET.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_NEXT_ENTRY_PACKET_G211C3R4L.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_BAKE_MANIFEST.json
artifacts/g211c3r4k/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4K.txt
```

Forbidden output:

```text
artifacts/g211c3r4k/ASH_BASETRAIN_GPU_70K_G211C3R4K_NEXT_ENTRY_PACKET_G211C4.json
```

## PASS Criteria

```text
PASS-01 R4J PASS marker found
PASS-02 R4J closeout_verdict = MEASUREMENT_HYGIENE_CLOSEOUT_COMPLETE
PASS-03 R4J closeout_class = MEASUREMENT_HYGIENE_CLOSED
PASS-04 R4J fresh_clean_speedup_probe_recommended=true
PASS-05 R4J c3_stop_perf_loss_retained=true
PASS-06 R4J promotion_stop_retained=true
PASS-07 G211C4 entry packet absent
PASS-08 fresh clean speedup probe plan written
PASS-09 timing authority contract written
PASS-10 probe shape plan written
PASS-11 contamination guard plan written
PASS-12 operator review packet written
PASS-13 route policy review packet written
PASS-14 probe plan verdict selected exactly once
PASS-15 probe plan class selected exactly once
PASS-16 primary timing authority = READBACK_FREE_DISPATCH_TIMESTAMP
PASS-17 correctness authority = SINGLE_FINAL_MAP_PARITY_CHECK
PASS-18 per-iteration map forbidden in measured interval
PASS-19 artifact write forbidden in measured interval
PASS-20 promotion stop retained
PASS-21 runtime_splice_allowed=false
PASS-22 promotion_allowed=false
PASS-23 G211C3R4L entry packet generated
PASS-24 G211C4 entry packet not generated
PASS-25 forbidden mutation seal passed
PASS-26 PASS marker printed
```

## PASS Meaning

PASS means G211C3R4K prepared a fresh clean speedup probe plan after measurement hygiene closeout, using readback-free dispatch timing and single-final-map parity requirements, while preserving no runtime splice, no promotion, and no G211C4 entry.

PASS does not mean TensorCube is faster. PASS does not mean fresh clean speedup probe has run. PASS does not mean promotion can reopen. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean production acceleration exists. PASS does not mean TensorCore is used.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4K fresh clean speedup probe plan

- Add fresh clean speedup probe planning gate
- Require R4J measurement hygiene closeout as entry authority
- Define readback-free dispatch timing authority
- Require single-final-map parity check
- Forbid per-iteration map and artifact write contamination in measured interval
- Preserve B0/B1/B5 required shape set
- Emit operator review and route policy review packets
- Route to G211C3R4L fresh clean speedup probe execution
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
