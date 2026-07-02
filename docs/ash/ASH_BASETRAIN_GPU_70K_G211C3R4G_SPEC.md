# ASH-BASETRAIN-GPU-70K-G211C3R4G

## Poll Map Wait Isolation / Readback-Free Dispatch Attribution Recovery / No Runtime Splice No Promotion Reopen

Seal: Poll Map Wait Isolation Only / Readback-Free Dispatch Attribution Recovery Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4G` consumes the G211C3R4F poll/map contamination outputs as its primary input authority and preserves the G211C3 `STOP_PERF_LOSS` result.

`70K-G211C3R4G` may only pass when R4F PASS is present, the R4F-R1 next-gate reader hotfix receipt is present, `normalization_verdict = POLL_MAP_CONTAMINATION_DOMINANT`, `normalization_class = POLL_MAP_WAIT_DOMINANT`, `r4e_attribution_retained = false`, R4E attribution context is present, R4B dispatch-only context is present, B0/B1/B5 isolation rows are present, parity remains pass, timestamp stability is retained, the G211C3 promotion stop is retained, and no G211C4 entry packet exists.

`70K-G211C3R4G` must not mutate the TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not implement TensorCube kernel optimization, must not rewrite a production WGSL kernel, must not change production tile/workgroup/padding policy, must not rerun promotion, and must not claim TensorCore usage, speedup, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R4F
Readback Poll Map Split /
Attribution Normalization Gate /
No Runtime Splice No Promotion Reopen
```

Required predecessor evidence:

```text
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_READBACK_POLL_MAP_SPLIT.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_R1_NEXT_GATE_READER_HOTFIX.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_POST_DISPATCH_TIMING_MATRIX.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_ATTRIBUTION_NORMALIZATION.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_CONTAMINATION_RATIO_SUMMARY.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_R4E_VERDICT_RETENTION_AUDIT.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_NEXT_ENTRY_PACKET_G211C3R4G.json
artifacts/g211c3r4f/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4F.txt
```

Reference evidence:

```text
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_KERNEL_TILE_PADDING_ATTRIBUTION.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_ATTRIBUTION_SUMMARY.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_TILE_UTILIZATION_MATRIX.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_R1_ACCEPT_PAIR_HOTFIX.json
artifacts/g211c3r4e/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4E.txt
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_DISPATCH_ONLY_TIMING_PROBE.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_DISPATCH_ONLY_TIMING_MATRIX.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_TIMESTAMP_STABILITY_AUDIT.json
```

Forbidden evidence:

```text
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r3/ASH_BASETRAIN_GPU_70K_G211C3R3_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_NEXT_ENTRY_PACKET_G211C4.json
```

## Purpose

G211C3R4G isolates the poll/map wait contamination reported by R4F and recovers or audits readback-free dispatch attribution before any odd-shape/tail attribution recheck.

G211C3R4G proves only this:

```text
R4F poll/map contamination dominance was present
R4F-R1 next-gate reader hotfix was present
timestamp-only dispatch, single-final-map, per-iteration-map, and no-artifact-write paths were audited
poll/map wait delta and recovery ratio were computed
R4E mixed attribution was recovered, rejected, or held for R4H
parity remained pass
runtime splice and promotion remained closed
G211C4 entry remained absent
```

G211C3R4G does not optimize TensorCube. G211C3R4G does not rerun promotion. G211C3R4G does not authorize G211C4.

## Required Probe Shapes

```text
B0 = [8, 8, 8]
B1 = [16, 16, 8]
B5 = [17, 31, 65]
```

Optional context:

```text
B2 = [16, 16, 64]
B5_PAD8 = [24, 32, 72]
B5_NEAR_EVEN = [16, 32, 64]
```

## Poll Map Isolation Paths

```text
TIMESTAMP_ONLY_DISPATCH
SINGLE_FINAL_MAP
PER_ITERATION_MAP
NO_ARTIFACT_WRITE_TIMING
```

`TIMESTAMP_ONLY_DISPATCH` is the readback-free diagnostic authority. `SINGLE_FINAL_MAP` verifies correctness without per-iteration map wait. `PER_ITERATION_MAP` reproduces the R4F contamination path. `NO_ARTIFACT_WRITE_TIMING` excludes JSON/artifact write from timing.

## Required Metrics

```text
gpu_dispatch_timestamp_p50_ms
gpu_dispatch_timestamp_p95_ms
queue_submit_wall_p50_ms
device_poll_wait_p50_ms
map_async_issue_p50_ms
map_async_wait_p50_ms
mapped_range_read_p50_ms
buffer_unmap_p50_ms
artifact_write_p50_ms
total_path_wall_p50_ms
timestamp_valid
parity_pass
```

Derived metrics:

```text
poll_map_wait_ms = device_poll_wait_p50_ms + map_async_wait_p50_ms
poll_map_delta_ms = candidate_poll_map_wait_ms - baseline_poll_map_wait_ms
readback_free_dispatch_delta_ms = candidate_timestamp_only_dispatch_p50_ms - baseline_timestamp_only_dispatch_p50_ms
contaminated_path_delta_ms = candidate_per_iteration_map_total_p50_ms - baseline_per_iteration_map_total_p50_ms
poll_map_recovery_ratio = 1.0 - (abs(readback_free_dispatch_delta_ms) / max(abs(contaminated_path_delta_ms), epsilon))
epsilon = 0.000001
```

## Recovery Classes

```text
READBACK_FREE_DISPATCH_RECOVERED
POLL_MAP_WAIT_CONFIRMED_DOMINANT
POLL_MAP_WAIT_PARTIAL_CONTAMINATION
DISPATCH_LOSS_PERSISTS_AFTER_POLL_MAP_REMOVAL
R4E_MIXED_ATTRIBUTION_RECOVERED
R4E_MIXED_ATTRIBUTION_REJECTED_BY_POLL_MAP
R4E_MIXED_ATTRIBUTION_HELD_FOR_R4H
MAP_MINIMIZATION_INCOMPLETE
RECOVERY_TIMESTAMP_UNSTABLE
RECOVERY_PARITY_FAILED
INCONCLUSIVE
```

## Verdict Values

```text
POLL_MAP_WAIT_ISOLATED
READBACK_FREE_DISPATCH_ATTRIBUTION_RECOVERED
R4E_MIXED_ATTRIBUTION_RECOVERED
R4E_MIXED_ATTRIBUTION_REJECTED_BY_POLL_MAP
R4E_MIXED_ATTRIBUTION_HELD_FOR_R4H
DISPATCH_LOSS_PERSISTS_AFTER_POLL_MAP_REMOVAL
POLL_MAP_ISOLATION_INCOMPLETE
RECOVERY_TIMESTAMP_UNSTABLE
RECOVERY_PARITY_FAILED
INCONCLUSIVE
```

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4g_poll_map_wait_isolation.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4g_poll_map_wait_isolation
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
--out-dir artifacts/g211c3r4g
--probe-shapes B0,B1,B5
--paths TIMESTAMP_ONLY_DISPATCH,SINGLE_FINAL_MAP,PER_ITERATION_MAP,NO_ARTIFACT_WRITE_TIMING
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4G_POLL_MAP_WAIT_ISOLATION
```

Expected stdout fields:

```text
patch_id=ASH-BASETRAIN-GPU-70K-G211C3R4G
timestamp_query_status=TIMESTAMP_QUERY_AVAILABLE
recovery_verdict=<...>
recovery_class=<...>
required_probe_shape_count=3
all_required_probe_shapes_measured=<true|false>
timestamp_only_dispatch_measured=<true|false>
single_final_map_measured=<true|false>
per_iteration_map_measured=<true|false>
artifact_write_excluded_path_measured=<true|false>
poll_map_wait_confirmed_dominant=<true|false>
readback_free_dispatch_recovered=<true|false>
r4e_mixed_attribution_recovered=<true|false>
r4e_mixed_attribution_rejected_by_poll_map=<true|false>
r4e_mixed_attribution_held_for_r4h=<true|false>
parity_pass=<true|false>
runtime_splice_allowed=false
promotion_allowed=false
g211c4_entry_generated=false
next_gate=ASH-BASETRAIN-GPU-70K-G211C3R4H
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r4g` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_POLL_MAP_WAIT_ISOLATION.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_READBACK_FREE_DISPATCH_MATRIX.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_PATH_COMPARISON_MATRIX.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_POLL_MAP_RECOVERY_SUMMARY.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_R4E_ATTRIBUTION_RECOVERY_AUDIT.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_NEXT_ENTRY_PACKET_G211C3R4H.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_BAKE_MANIFEST.json
artifacts/g211c3r4g/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4G.txt
```

Forbidden output:

```text
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_NEXT_ENTRY_PACKET_G211C4.json
```

## PASS Criteria

```text
PASS-01 R4F PASS marker found
PASS-02 R4F-R1 next gate reader hotfix receipt found
PASS-03 R4F normalization_verdict = POLL_MAP_CONTAMINATION_DOMINANT
PASS-04 R4F normalization_class = POLL_MAP_WAIT_DOMINANT
PASS-05 R4F r4e_attribution_retained=false
PASS-06 R4E attribution context found
PASS-07 R4B dispatch-only context found
PASS-08 G211C4 entry packet absent
PASS-09 required probe shapes B0/B1/B5 present
PASS-10 required paths TIMESTAMP_ONLY_DISPATCH, SINGLE_FINAL_MAP, PER_ITERATION_MAP, NO_ARTIFACT_WRITE_TIMING present
PASS-11 readback-free dispatch matrix written
PASS-12 path comparison matrix written
PASS-13 poll map recovery summary written
PASS-14 R4E attribution recovery audit written
PASS-15 recovery verdict selected exactly once
PASS-16 recovery class selected exactly once
PASS-17 timestamp stability audit written
PASS-18 parity remains pass
PASS-19 promotion stop retained
PASS-20 runtime_splice_allowed=false
PASS-21 promotion_allowed=false
PASS-22 G211C3R4H entry packet generated
PASS-23 G211C4 entry packet not generated
PASS-24 forbidden mutation seal passed
PASS-25 PASS marker printed
```

## PASS Meaning

PASS means R4G isolated poll/map wait contamination and produced readback-free dispatch attribution recovery evidence after R4F reported poll/map contamination dominance.

PASS does not mean TensorCube is faster. PASS does not mean TensorCube timing hygiene is fully repaired. PASS does not mean TensorCube optimization has been applied. PASS does not mean promotion is reopened. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean TensorCore is used.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4G poll map wait isolation

- Add poll map wait isolation gate
- Require R4F poll/map contamination dominant verdict as entry authority
- Compare timestamp-only dispatch, single-final-map, per-iteration-map, and no-artifact-write paths
- Compute poll/map wait delta and recovery ratio
- Audit whether R4E mixed attribution is recovered, rejected, or held for R4H
- Route to G211C3R4H odd/tail attribution recheck
- Preserve G211C3 STOP_PERF_LOSS and promotion stop
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
