# ASH-BASETRAIN-GPU-70K-G211C3R4E

## Kernel Tile Padding Attribution / Odd Shape And Tile Utilization Probe / No Runtime Splice No Promotion Reopen

Seal: Kernel Tile Padding Attribution Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4E` consumes the G211C3R4D-R2 audit outputs as its entry authority and preserves the G211C3 `STOP_PERF_LOSS` result.

`70K-G211C3R4E` may only pass when G211C3R4D-R2 PASS is present, the G211C3R4D-R2 next entry packet to G211C3R4E is present, `r4e_entry_policy = ALLOW_R4E_CONFIRMED`, `audit_verdict = R4D_R2_CONSISTENCY_CONFIRMED`, R4C small-shape kernel/tile-loss context is present, R4B dispatch-only timing context is present, B0/B1/B5 attribution is captured, parity remains pass, the G211C3 promotion stop is retained, and no G211C4 entry packet exists.

`70K-G211C3R4E` must not mutate the TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not implement TensorCube kernel optimization, must not rewrite a production WGSL kernel, must not change production tile/workgroup layout, must not rerun promotion, and must not claim TensorCore usage, speedup, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R4D-R2
Reuse Recovery Delta Sign Audit /
Setup Dominance Verdict Consistency Seal /
No Timing Rerun No Artifact Rewrite
```

Required predecessor evidence:

```text
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_REUSE_DELTA_SIGN_AUDIT.json
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_SETUP_DOMINANCE_CONSISTENCY_SEAL.json
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_R4E_ENTRY_POLICY.json
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_FORBIDDEN_REWRITE_SEAL.json
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_NEXT_ENTRY_PACKET_G211C3R4E.json
artifacts/g211c3r4d_r2/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4D_R2.txt
```

R4E also references R4D, R4C, R4B, and G211C3 promotion-stop receipts. These are context authority only and must not be rewritten.

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
```

## Purpose

G211C3R4E measures or audits whether the remaining TensorCube candidate loss is attributable to kernel tile structure, odd shape padding, tail workgroup utilization, K-loop tail, or a mixed setup/kernel loss after R4D-R2 confirmed the setup dominance verdict.

G211C3R4E proves only this:

```text
G211C3 STOP_PERF_LOSS was preserved
G211C3R4D-R2 confirmed R4E entry was accepted as authority
B0/B1/B5 tile utilization and padding pressure were audited
R4B dispatch-only timing context was used for hot dispatch comparison
odd shape B5 diagnostic pair geometry was audited
primary attribution class was selected
parity remained pass
runtime splice and promotion remained closed
```

G211C3R4E does not optimize TensorCube. G211C3R4E does not rerun promotion. G211C3R4E does not authorize G211C4.

## Required Probe Shapes

```text
B0 = [8, 8, 8]       SMALL_EXACT_TILE
B1 = [16, 16, 8]     SMALL_MULTI_TILE
B5 = [17, 31, 65]    ODD_EDGE_SHAPE
```

Optional context shape:

```text
B2 = [16, 16, 64]    K_LOOP_HEAVY_SHAPE
```

Diagnostic tile assumption:

```text
tile_m = 8
tile_n = 8
tile_k = 8
```

This is a diagnostic assumption, not a production tile mutation.

## Tile And Padding Metrics

```text
tile_rows = ceil(m / tile_m)
tile_cols = ceil(n / tile_n)
tile_k_blocks = ceil(k / tile_k)
padded_m = tile_rows * tile_m
padded_n = tile_cols * tile_n
padded_k = tile_k_blocks * tile_k
active_output_cells = m * n
padded_output_cells = padded_m * padded_n
output_cell_utilization_ratio = active_output_cells / padded_output_cells
output_padding_waste_ratio = 1.0 - output_cell_utilization_ratio
k_utilization_ratio = k / padded_k
k_padding_waste_ratio = 1.0 - k_utilization_ratio
combined_padding_pressure = 1.0 - (output_cell_utilization_ratio * k_utilization_ratio)
```

These are diagnostic pressure metrics, not speedup claims.

## Controlled Shape Pair Probes

```text
B5 = [17, 31, 65]
B5_PAD8 = [24, 32, 72]
B5_NEAR_EVEN = [16, 32, 64]
```

Controlled shape pair outputs are diagnostic only. They must not be represented as production benchmark results and must not reopen promotion.

## Attribution Classes

G211C3R4E must select exactly one primary attribution class.

```text
TILE_PADDING_ATTRIBUTION_CAPTURED
ODD_SHAPE_PADDING_DOMINANT
SMALL_TILE_UTILIZATION_LOSS_DOMINANT
K_LOOP_TAIL_LOSS_DOMINANT
KERNEL_INSTRUCTION_OR_MEMORY_LOSS_DOMINANT
SETUP_AND_KERNEL_MIXED_LOSS
ATTRIBUTION_INCOMPLETE
ATTRIBUTION_PARITY_FAILED
ATTRIBUTION_TIMESTAMP_UNSTABLE
INCONCLUSIVE
```

`SETUP_AND_KERNEL_MIXED_LOSS` is preferred when R4D-R2 setup dominance is confirmed and R4E also detects remaining hot-dispatch kernel/tile/padding loss.

## Verdict Values

G211C3R4E must produce exactly one attribution verdict.

```text
KERNEL_TILE_PADDING_ATTRIBUTION_CAPTURED
ODD_SHAPE_PADDING_DOMINANT
SMALL_TILE_UTILIZATION_LOSS_DOMINANT
K_LOOP_TAIL_LOSS_DOMINANT
KERNEL_INSTRUCTION_OR_MEMORY_LOSS_DOMINANT
SETUP_AND_KERNEL_MIXED_LOSS
ATTRIBUTION_MATRIX_INCOMPLETE
ATTRIBUTION_TIMESTAMP_UNSTABLE
ATTRIBUTION_PARITY_FAILED
INCONCLUSIVE
```

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4e_kernel_tile_padding_attribution.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4e_kernel_tile_padding_attribution
```

Alternative command from `crates/base_train`:

```powershell
cargo run --bin ash_basetrain_gpu_70k_g211c3r4e_kernel_tile_padding_attribution
```

Optional arguments:

```text
--g211c3-dir artifacts/g211c3
--g211c3r4b-dir artifacts/g211c3r4b
--g211c3r4c-dir artifacts/g211c3r4c
--g211c3r4d-dir artifacts/g211c3r4d
--g211c3r4d-r2-dir artifacts/g211c3r4d_r2
--out-dir artifacts/g211c3r4e
--probe-shapes B0,B1,B5
--diagnostic-pairs B5_PAD8,B5_NEAR_EVEN
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4E_KERNEL_TILE_PADDING_ATTRIBUTION
```

Expected stdout fields:

```text
patch_id=ASH-BASETRAIN-GPU-70K-G211C3R4E
timestamp_query_status=TIMESTAMP_QUERY_AVAILABLE
attribution_verdict=<...>
primary_attribution_class=<...>
required_probe_shape_count=3
all_required_probe_shapes_measured=<true|false>
controlled_shape_pairs_measured=<true|false>
tile_utilization_matrix_written=<true|false>
odd_shape_padding_probe_written=<true|false>
parity_pass=<true|false>
runtime_splice_allowed=false
promotion_allowed=false
g211c4_entry_generated=false
next_gate=ASH-BASETRAIN-GPU-70K-G211C3R4F
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r4e` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_KERNEL_TILE_PADDING_ATTRIBUTION.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_TILE_UTILIZATION_MATRIX.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_ODD_SHAPE_PADDING_PROBE.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_CONTROLLED_SHAPE_PAIR_AUDIT.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_ATTRIBUTION_SUMMARY.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_NEXT_ENTRY_PACKET_G211C3R4F.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_BAKE_MANIFEST.json
artifacts/g211c3r4e/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4E.txt
```

Forbidden output:

```text
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_NEXT_ENTRY_PACKET_G211C4.json
```

## PASS Criteria

```text
PASS-01 R4D-R2 PASS marker found
PASS-02 R4D-R2 R4E entry policy found
PASS-03 r4e_entry_policy = ALLOW_R4E_CONFIRMED
PASS-04 G211C3 STOP_PERF_LOSS retained
PASS-05 R4B dispatch-only matrix found
PASS-06 R4C small-shape kernel/tile loss context found
PASS-07 R4D setup dominance context found
PASS-08 G211C4 entry packet absent
PASS-09 required probe shapes B0/B1/B5 present
PASS-10 tile utilization matrix written
PASS-11 odd shape padding probe written
PASS-12 controlled shape pair audit written
PASS-13 attribution summary written
PASS-14 attribution verdict selected exactly once
PASS-15 primary attribution class selected exactly once
PASS-16 timestamp stability audit written
PASS-17 parity remains pass
PASS-18 promotion stop retained
PASS-19 runtime_splice_allowed=false
PASS-20 promotion_allowed=false
PASS-21 G211C3R4F entry packet generated
PASS-22 G211C4 entry packet not generated
PASS-23 forbidden mutation seal passed
PASS-24 PASS marker printed
```

## PASS Meaning

PASS means G211C3R4E captured or explicitly audited kernel tile padding attribution for required shapes B0, B1, and B5, while preserving R4D-R2 confirmed entry policy and promotion stop.

PASS does not mean TensorCube is faster. PASS does not mean TensorCube timing hygiene is fully repaired. PASS does not mean TensorCube optimization has been applied. PASS does not mean TensorCube promotion is reopened. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean production acceleration exists. PASS does not mean TensorCore is used. PASS does not mean diagnostic shape pairs are production benchmark results.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4E kernel tile padding attribution

- Add kernel tile padding attribution gate
- Require R4D-R2 confirmed R4E entry policy as authority
- Inspect B0/B1/B5 tile utilization and padding pressure
- Add odd shape B5 diagnostic padded pair audit
- Compute output cell utilization, K-tail utilization, and combined padding pressure
- Classify small tile, odd padding, K-tail, kernel memory, or mixed setup/kernel loss
- Preserve G211C3 STOP_PERF_LOSS and promotion stop
- Route to G211C3R4F without G211C4 entry
- Preserve no runtime splice, no production route, no promotion
```
