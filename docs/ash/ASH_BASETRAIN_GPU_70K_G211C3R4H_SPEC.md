# ASH-BASETRAIN-GPU-70K-G211C3R4H

## Odd Tail Padding Recheck / Post Poll-Map Clean Attribution / No Runtime Splice No Promotion Reopen

Seal: Odd Tail Padding Recheck Only / Post Poll-Map Clean Attribution Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4H` consumes the G211C3R4G poll/map wait isolation outputs as its primary input authority and preserves the G211C3 `STOP_PERF_LOSS` result.

`70K-G211C3R4H` may only pass when R4G PASS is present, `recovery_verdict = POLL_MAP_WAIT_ISOLATED`, `recovery_class = POLL_MAP_WAIT_CONFIRMED_DOMINANT`, `readback_free_dispatch_recovered = true`, `r4e_mixed_attribution_held_for_r4h = true`, R4G readback-free dispatch matrix is present, R4E tile/odd-tail context is present, B0/B1/B5 clean dispatch rows are present, parity remains pass, timestamp stability is retained, the G211C3 promotion stop is retained, and no G211C4 entry packet exists.

`70K-G211C3R4H` must not mutate the TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not implement TensorCube kernel optimization, must not rewrite a production WGSL kernel, must not change production tile/workgroup/padding policy, must not rerun promotion, and must not claim TensorCore usage, speedup, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R4G
Poll Map Wait Isolation /
Readback-Free Dispatch Attribution Recovery /
No Runtime Splice No Promotion Reopen
```

Required predecessor evidence:

```text
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_POLL_MAP_WAIT_ISOLATION.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_READBACK_FREE_DISPATCH_MATRIX.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_PATH_COMPARISON_MATRIX.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_POLL_MAP_RECOVERY_SUMMARY.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_R4E_ATTRIBUTION_RECOVERY_AUDIT.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_NEXT_ENTRY_PACKET_G211C3R4H.json
artifacts/g211c3r4g/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4G.txt
```

Reference evidence:

```text
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_KERNEL_TILE_PADDING_ATTRIBUTION.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_ATTRIBUTION_SUMMARY.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_TILE_UTILIZATION_MATRIX.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_ODD_SHAPE_PADDING_PROBE.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_CONTROLLED_SHAPE_PAIR_AUDIT.json
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
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_NEXT_ENTRY_PACKET_G211C4.json
```

## Purpose

G211C3R4H rechecks B5 odd shape, K-tail, output padding, and tile-utilization residual after R4G isolated poll/map wait contamination.

G211C3R4H proves only this:

```text
R4G poll/map wait isolation was present
R4G readback-free dispatch was recovered
B0/B1/B5 clean dispatch deltas were extracted
B5 output padding, K-tail, and combined padding pressure were computed
B5 clean residual was classified
R4E mixed attribution was recovered, rejected, or held for R4I
parity remained pass
runtime splice and promotion remained closed
G211C4 entry remained absent
```

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

## Clean Dispatch Metrics

R4H uses R4G `READBACK_FREE_DISPATCH_MATRIX` as the clean dispatch authority.

```text
baseline_clean_dispatch_p50_ms
candidate_clean_dispatch_p50_ms
clean_dispatch_delta_ms = candidate_clean_dispatch_p50_ms - baseline_clean_dispatch_p50_ms
clean_dispatch_ratio = candidate_clean_dispatch_p50_ms / max(baseline_clean_dispatch_p50_ms, epsilon)
epsilon = 0.000001
```

## Odd Tail Padding Metrics

Diagnostic tile assumption:

```text
tile_m = 8
tile_n = 8
tile_k = 8
```

Derived metrics:

```text
padded_m = ceil(m / tile_m) * tile_m
padded_n = ceil(n / tile_n) * tile_n
padded_k = ceil(k / tile_k) * tile_k
output_actual_cells = m * n
output_padded_cells = padded_m * padded_n
output_padding_cells = output_padded_cells - output_actual_cells
output_padding_ratio = output_padding_cells / max(output_padded_cells, 1)
k_tail_cells = padded_k - k
k_tail_ratio = k_tail_cells / max(padded_k, 1)
combined_padding_pressure = 1.0 - ((output_actual_cells * k) / max(output_padded_cells * padded_k, 1))
b5_clean_residual_loss_ms = B5.clean_dispatch_delta_ms - median(B0.clean_dispatch_delta_ms, B1.clean_dispatch_delta_ms)
b5_clean_residual_ratio = B5.clean_dispatch_ratio / max(median(B0.clean_dispatch_ratio, B1.clean_dispatch_ratio), epsilon)
```

## Recheck Classes

```text
POST_POLL_MAP_CLEAN_ATTRIBUTION_CAPTURED
B5_ODD_PADDING_LOSS_CONFIRMED
B5_K_TAIL_LOSS_CONFIRMED
B5_TILE_UTILIZATION_LOSS_CONFIRMED
B5_ODD_TAIL_COMBINED_LOSS_CONFIRMED
B5_CLEAN_RESIDUAL_LOW
R4E_MIXED_ATTRIBUTION_RECOVERED
R4E_MIXED_ATTRIBUTION_REJECTED
R4E_MIXED_ATTRIBUTION_HELD_FOR_R4I
ODD_TAIL_RECHECK_INCOMPLETE
ODD_TAIL_TIMESTAMP_UNSTABLE
ODD_TAIL_PARITY_FAILED
INCONCLUSIVE
```

## Verdict Values

```text
POST_POLL_MAP_CLEAN_ATTRIBUTION_CAPTURED
B5_ODD_PADDING_LOSS_CONFIRMED
B5_K_TAIL_LOSS_CONFIRMED
B5_TILE_UTILIZATION_LOSS_CONFIRMED
B5_ODD_TAIL_COMBINED_LOSS_CONFIRMED
B5_CLEAN_RESIDUAL_LOW
R4E_MIXED_ATTRIBUTION_RECOVERED
R4E_MIXED_ATTRIBUTION_REJECTED
R4E_MIXED_ATTRIBUTION_HELD_FOR_R4I
ODD_TAIL_RECHECK_INCOMPLETE
ODD_TAIL_TIMESTAMP_UNSTABLE
ODD_TAIL_PARITY_FAILED
INCONCLUSIVE
```

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4h_odd_tail_padding_recheck.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4h_odd_tail_padding_recheck
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
--out-dir artifacts/g211c3r4h
--probe-shapes B0,B1,B5
--tile-m 8
--tile-n 8
--tile-k 8
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4H_ODD_TAIL_PADDING_RECHECK
```

Expected stdout fields:

```text
patch_id=ASH-BASETRAIN-GPU-70K-G211C3R4H
timestamp_query_status=TIMESTAMP_QUERY_AVAILABLE
recheck_verdict=<...>
recheck_class=<...>
required_probe_shape_count=3
all_required_probe_shapes_measured=<true|false>
clean_dispatch_matrix_written=<true|false>
odd_tail_padding_pressure_matrix_written=<true|false>
b5_residual_summary_written=<true|false>
b5_clean_residual_present=<true|false>
b5_clean_residual_low=<true|false>
b5_odd_padding_loss_confirmed=<true|false>
b5_k_tail_loss_confirmed=<true|false>
b5_tile_utilization_loss_confirmed=<true|false>
b5_odd_tail_combined_loss_confirmed=<true|false>
r4e_mixed_attribution_recovered=<true|false>
r4e_mixed_attribution_rejected=<true|false>
r4e_mixed_attribution_held_for_r4i=<true|false>
parity_pass=<true|false>
runtime_splice_allowed=false
promotion_allowed=false
g211c4_entry_generated=false
next_gate=ASH-BASETRAIN-GPU-70K-G211C3R4I
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r4h` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_ODD_TAIL_PADDING_RECHECK.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_CLEAN_DISPATCH_ATTRIBUTION_MATRIX.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_ODD_TAIL_PADDING_PRESSURE_MATRIX.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_B5_RESIDUAL_SUMMARY.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_R4E_MIXED_ATTRIBUTION_RECHECK_AUDIT.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_NEXT_ENTRY_PACKET_G211C3R4I.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_BAKE_MANIFEST.json
artifacts/g211c3r4h/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4H.txt
```

Forbidden output:

```text
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_NEXT_ENTRY_PACKET_G211C4.json
```

## PASS Criteria

```text
PASS-01 R4G PASS marker found
PASS-02 R4G recovery_verdict = POLL_MAP_WAIT_ISOLATED
PASS-03 R4G recovery_class = POLL_MAP_WAIT_CONFIRMED_DOMINANT
PASS-04 R4G readback_free_dispatch_recovered=true
PASS-05 R4G r4e_mixed_attribution_held_for_r4h=true
PASS-06 R4E attribution context found
PASS-07 R4E odd/tail/padding context found
PASS-08 G211C4 entry packet absent
PASS-09 required probe shapes B0/B1/B5 present
PASS-10 clean dispatch attribution matrix written
PASS-11 odd tail padding pressure matrix written
PASS-12 B5 residual summary written
PASS-13 R4E mixed attribution recheck audit written
PASS-14 recheck verdict selected exactly once
PASS-15 recheck class selected exactly once
PASS-16 timestamp stability audit written
PASS-17 parity remains pass
PASS-18 promotion stop retained
PASS-19 runtime_splice_allowed=false
PASS-20 promotion_allowed=false
PASS-21 G211C3R4I entry packet generated
PASS-22 G211C4 entry packet not generated
PASS-23 forbidden mutation seal passed
PASS-24 PASS marker printed
```

## PASS Meaning

PASS means R4H rechecked B5 odd/tail/padding attribution using post poll-map clean dispatch evidence and produced a clean attribution verdict without runtime splice, promotion, or G211C4 entry.

PASS does not mean TensorCube is faster. PASS does not mean TensorCube timing hygiene is fully repaired. PASS does not mean TensorCube optimization has been applied. PASS does not mean promotion is reopened. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean TensorCore is used.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4H odd tail padding recheck

- Add post poll-map clean attribution recheck gate
- Require R4G poll/map wait isolation as entry authority
- Recheck B0/B1/B5 clean dispatch deltas
- Compute B5 output padding, K-tail, and combined padding pressure
- Emit B5 clean residual summary
- Audit whether R4E mixed attribution is recovered, rejected, or held for R4I
- Route to G211C3R4I clean attribution decision ledger
- Preserve G211C3 STOP_PERF_LOSS and promotion stop
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
