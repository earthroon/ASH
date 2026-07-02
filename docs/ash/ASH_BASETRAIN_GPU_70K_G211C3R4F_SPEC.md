# ASH-BASETRAIN-GPU-70K-G211C3R4F

## Readback Poll Map Split / Attribution Normalization Gate / No Runtime Splice No Promotion Reopen

Seal: Readback Poll Map Split Only / Attribution Normalization Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4F` consumes the G211C3R4E attribution outputs as its primary input authority and preserves the G211C3 `STOP_PERF_LOSS` result.

`70K-G211C3R4F` may only pass when R4E PASS is present, the R4E-R1 accept-pair hotfix receipt is present, `attribution_verdict = SETUP_AND_KERNEL_MIXED_LOSS`, `primary_attribution_class = SETUP_AND_KERNEL_MIXED_LOSS`, R4B dispatch-only timing context is present, B0/B1/B5 normalization rows are present, parity remains pass, timestamp stability is retained, the G211C3 promotion stop is retained, and no G211C4 entry packet exists.

`70K-G211C3R4F` must not mutate the TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not implement TensorCube kernel optimization, must not rewrite a production WGSL kernel, must not change production tile/workgroup/padding policy, must not rerun promotion, and must not claim TensorCore usage, speedup, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R4E
Kernel Tile Padding Attribution /
Odd Shape And Tile Utilization Probe /
No Runtime Splice No Promotion Reopen
```

Required predecessor evidence:

```text
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_KERNEL_TILE_PADDING_ATTRIBUTION.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_R1_ACCEPT_PAIR_HOTFIX.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_TILE_UTILIZATION_MATRIX.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_ODD_SHAPE_PADDING_PROBE.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_CONTROLLED_SHAPE_PAIR_AUDIT.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_ATTRIBUTION_SUMMARY.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_NEXT_ENTRY_PACKET_G211C3R4F.json
artifacts/g211c3r4e/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4E.txt
```

Reference evidence:

```text
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_DISPATCH_ONLY_TIMING_PROBE.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_DISPATCH_ONLY_TIMING_MATRIX.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_READBACK_POLLUTION_SPLIT.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_SETUP_OVERHEAD_ISOLATION_PROBE.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_SETUP_COMPONENT_SPLIT.json
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_REUSE_DELTA_SIGN_AUDIT.json
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_R4E_ENTRY_POLICY.json
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
```

## Purpose

G211C3R4F separates the R4E `SETUP_AND_KERNEL_MIXED_LOSS` attribution from readback, copy, poll, map, unmap, and artifact-write measurement tail cost.

G211C3R4F proves only this:

```text
R4E mixed attribution was present
R4E-R1 accept-pair hotfix was present
B0/B1/B5 post-dispatch timing rows were produced
readback and artifact contamination ratios were computed
R4E attribution was retained, softened, or routed to R4G
parity remained pass
runtime splice and promotion remained closed
G211C4 entry remained absent
```

G211C3R4F does not optimize TensorCube. G211C3R4F does not rerun promotion. G211C3R4F does not authorize G211C4.

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

R4F does not alter the shape set, diagnostic pair geometry, production tile size, or production workgroup layout.

## Readback Poll Map Split Metrics

For each shape and path, R4F records:

```text
gpu_dispatch_only_ms
queue_submit_wall_ms
copy_buffer_to_buffer_encode_ms
copy_submit_wall_ms
device_poll_wait_ms
map_async_issue_ms
map_async_wait_ms
mapped_range_read_ms
buffer_unmap_ms
json_artifact_write_ms
total_readback_wall_ms
total_post_dispatch_wall_ms
total_wall_ms
```

`gpu_dispatch_only_ms` is the authority for GPU compute attribution.

```text
post_dispatch_overhead_ms = total_wall_ms - gpu_dispatch_only_ms
readback_inclusive_ms = gpu_dispatch_only_ms + copy_submit_wall_ms + device_poll_wait_ms + map_async_wait_ms + mapped_range_read_ms + buffer_unmap_ms
artifact_inclusive_ms = readback_inclusive_ms + json_artifact_write_ms
```

Artifact-inclusive timing must never be used for production speedup or kernel attribution.

## Normalization Metrics

```text
dispatch_only_candidate_loss_ms = candidate_gpu_dispatch_only_p50_ms - baseline_gpu_dispatch_only_p50_ms
readback_inclusive_candidate_loss_ms = candidate_readback_inclusive_p50_ms - baseline_readback_inclusive_p50_ms
artifact_inclusive_candidate_loss_ms = candidate_artifact_inclusive_p50_ms - baseline_artifact_inclusive_p50_ms
readback_contamination_ms = readback_inclusive_candidate_loss_ms - dispatch_only_candidate_loss_ms
artifact_contamination_ms = artifact_inclusive_candidate_loss_ms - readback_inclusive_candidate_loss_ms
readback_contamination_ratio = abs(readback_contamination_ms) / max(abs(readback_inclusive_candidate_loss_ms), epsilon)
artifact_contamination_ratio = abs(artifact_contamination_ms) / max(abs(artifact_inclusive_candidate_loss_ms), epsilon)
epsilon = 0.000001
```

## Normalization Classes

R4F must select exactly one normalization class.

```text
READBACK_POLL_MAP_SPLIT_CAPTURED
READBACK_CONTAMINATION_LOW
READBACK_CONTAMINATION_HIGH
POLL_MAP_WAIT_DOMINANT
ARTIFACT_WRITE_CONTAMINATION_DOMINANT
DISPATCH_ONLY_ATTRIBUTION_STABLE
R4E_ATTRIBUTION_RETAINED
R4E_ATTRIBUTION_SOFTENED_BY_READBACK
R4E_ATTRIBUTION_REQUIRES_R4G_ODD_PADDING_ISOLATION
NORMALIZATION_INCOMPLETE
NORMALIZATION_TIMESTAMP_UNSTABLE
NORMALIZATION_PARITY_FAILED
INCONCLUSIVE
```

## Verdict Values

R4F must produce exactly one normalization verdict.

```text
READBACK_POLL_MAP_SPLIT_CAPTURED
R4E_ATTRIBUTION_RETAINED
R4E_ATTRIBUTION_SOFTENED_BY_READBACK
POLL_MAP_CONTAMINATION_DOMINANT
ARTIFACT_WRITE_CONTAMINATION_DOMINANT
DISPATCH_ONLY_ATTRIBUTION_STABLE
NORMALIZATION_REQUIRES_R4G_ODD_PADDING_ISOLATION
NORMALIZATION_MATRIX_INCOMPLETE
NORMALIZATION_TIMESTAMP_UNSTABLE
NORMALIZATION_PARITY_FAILED
INCONCLUSIVE
```

Preferred safe verdict when mixed attribution remains stable and readback contamination is low:

```text
R4E_ATTRIBUTION_RETAINED
```

Preferred safe verdict when B5 remains ambiguous:

```text
NORMALIZATION_REQUIRES_R4G_ODD_PADDING_ISOLATION
```

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4f_readback_poll_map_split.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4f_readback_poll_map_split
```

Alternative command from `crates/base_train`:

```powershell
cargo run --bin ash_basetrain_gpu_70k_g211c3r4f_readback_poll_map_split
```

Optional arguments:

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
--out-dir artifacts/g211c3r4f
--probe-shapes B0,B1,B5
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4F_READBACK_POLL_MAP_SPLIT
```

Expected stdout fields:

```text
patch_id=ASH-BASETRAIN-GPU-70K-G211C3R4F
timestamp_query_status=TIMESTAMP_QUERY_AVAILABLE
normalization_verdict=<...>
normalization_class=<...>
required_probe_shape_count=3
all_required_probe_shapes_measured=<true|false>
post_dispatch_split_measured=<true|false>
readback_poll_map_split_measured=<true|false>
artifact_write_split_measured=<true|false>
r4e_attribution_retained=<true|false>
parity_pass=<true|false>
runtime_splice_allowed=false
promotion_allowed=false
g211c4_entry_generated=false
next_gate=ASH-BASETRAIN-GPU-70K-G211C3R4G
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r4f` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_READBACK_POLL_MAP_SPLIT.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_POST_DISPATCH_TIMING_MATRIX.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_ATTRIBUTION_NORMALIZATION.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_CONTAMINATION_RATIO_SUMMARY.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_R4E_VERDICT_RETENTION_AUDIT.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_NEXT_ENTRY_PACKET_G211C3R4G.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_BAKE_MANIFEST.json
artifacts/g211c3r4f/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4F.txt
```

Forbidden output:

```text
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_NEXT_ENTRY_PACKET_G211C4.json
```

## PASS Criteria

```text
PASS-01 R4E PASS marker found
PASS-02 R4E-R1 accept pair hotfix receipt found
PASS-03 R4E attribution summary found
PASS-04 R4E attribution_verdict = SETUP_AND_KERNEL_MIXED_LOSS
PASS-05 R4E primary_attribution_class = SETUP_AND_KERNEL_MIXED_LOSS
PASS-06 R4B dispatch-only timing matrix found
PASS-07 G211C4 entry packet absent
PASS-08 required probe shapes B0/B1/B5 present
PASS-09 post-dispatch timing matrix written
PASS-10 readback poll map split written
PASS-11 attribution normalization written
PASS-12 contamination ratio summary written
PASS-13 R4E verdict retention audit written
PASS-14 normalization verdict selected exactly once
PASS-15 normalization class selected exactly once
PASS-16 timestamp stability audit written
PASS-17 parity remains pass
PASS-18 promotion stop retained
PASS-19 runtime_splice_allowed=false
PASS-20 promotion_allowed=false
PASS-21 G211C3R4G entry packet generated
PASS-22 G211C4 entry packet not generated
PASS-23 forbidden mutation seal passed
PASS-24 PASS marker printed
```

## PASS Meaning

PASS means R4F split or normalized readback, poll, map, and artifact-write overhead from dispatch-only attribution, then sealed the R4E `SETUP_AND_KERNEL_MIXED_LOSS` verdict without runtime splice, promotion, or G211C4 entry.

PASS does not mean TensorCube is faster. PASS does not mean TensorCube timing hygiene is fully repaired. PASS does not mean TensorCube optimization has been applied. PASS does not mean promotion is reopened. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean TensorCore is used.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4F readback poll map split

- Add readback poll map split normalization gate
- Require R4E mixed attribution and R4E-R1 accept-pair hotfix as entry authority
- Split dispatch-only timing from copy, poll, map, unmap, and artifact-write timing
- Compute readback and artifact contamination ratios
- Normalize R4E SETUP_AND_KERNEL_MIXED_LOSS attribution
- Emit R4E verdict retention audit
- Route to G211C3R4G odd padding isolation
- Preserve G211C3 STOP_PERF_LOSS and promotion stop
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
