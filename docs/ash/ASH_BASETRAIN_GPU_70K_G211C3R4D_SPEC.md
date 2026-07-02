# ASH-BASETRAIN-GPU-70K-G211C3R4D

## Pipeline And Bind Group Reuse Split / Setup Overhead Isolation Probe / No Runtime Splice No Promotion Reopen

Seal: Setup Overhead Isolation Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4D` consumes the G211C3R4C repeated dispatch batch timing outputs as its entry authority and preserves the G211C3 `STOP_PERF_LOSS` result.

`70K-G211C3R4D` may only pass when G211C3R4C PASS is present, the G211C3R4C next entry packet to G211C3R4D is present, `timestamp_query_status = TIMESTAMP_QUERY_AVAILABLE`, `batch_timing_verdict = SMALL_SHAPE_KERNEL_OR_TILE_LOSS_REMAINS`, `small_shape_amortization_class = KERNEL_OR_TILE_LOSS_REMAINS`, B0/B1 setup split is captured, parity remains pass, the G211C3 promotion stop is retained, and no G211C4 entry packet exists.

`70K-G211C3R4D` must not mutate the TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not implement TensorCube kernel optimization, must not rewrite WGSL for production, must not change tile/workgroup layout for production, must not rerun promotion, and must not claim TensorCore usage, speedup, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R4C
Repeated Dispatch Batch Timing Crosscheck /
Small Shape Amortization Probe /
No Runtime Splice No Promotion Reopen
```

Required predecessor evidence:

```text
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_REPEATED_DISPATCH_BATCH_TIMING.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_SMALL_SHAPE_AMORTIZATION_MATRIX.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_BATCH_RECOVERY_SUMMARY.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_NEXT_ENTRY_PACKET_G211C3R4D.json
artifacts/g211c3r4c/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4C.txt
```

Required context evidence:

```text
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_DISPATCH_ONLY_TIMING_PROBE.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_DISPATCH_ONLY_TIMING_MATRIX.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_PROMOTION_STOP_PACKET.json
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
```

## Purpose

G211C3R4D isolates whether the remaining small-shape candidate loss is explained by pipeline creation, bind group creation, buffer allocation/reuse, command encoder setup, or whether the loss still remains in the hot GPU dispatch slice after setup is reused.

G211C3R4D proves only this:

```text
G211C3 STOP_PERF_LOSS was preserved
G211C3R4C kernel-or-tile-loss-remains verdict was accepted as entry authority
B0/B1 setup split was captured or explicitly audited
pipeline reuse was measured
bind group reuse was measured
buffer reuse was measured
command encoder split was measured
GPU timestamp dispatch-only timing remained the dispatch authority
parity remained pass
runtime splice and promotion remained closed
```

G211C3R4D does not optimize TensorCube. G211C3R4D does not rerun benchmark promotion. G211C3R4D does not authorize G211C4.

## Required Setup Probe Shapes

```text
B0 = [8, 8, 8]
B1 = [16, 16, 8]
```

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4d_setup_overhead_isolation_probe.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4d_setup_overhead_isolation_probe
```

Alternative command from `crates/base_train`:

```powershell
cargo run --bin ash_basetrain_gpu_70k_g211c3r4d_setup_overhead_isolation_probe
```

Optional arguments:

```text
--g211c3-dir artifacts/g211c3
--g211c3r4b-dir artifacts/g211c3r4b
--g211c3r4c-dir artifacts/g211c3r4c
--out-dir artifacts/g211c3r4d
--warmup-iterations 20
--measured-iterations 100
--probe-shapes B0,B1
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4D_SETUP_OVERHEAD_ISOLATION_PROBE
```

## Setup Split Contract

G211C3R4D compares these modes:

```text
COLD_ALL
WARM_PIPELINE_ONLY
WARM_BIND_GROUP_ONLY
WARM_BUFFER_REUSE
HOT_DISPATCH_ONLY
```

Required timing components for baseline and TensorCube candidate:

```text
pipeline_create_ms
bind_group_layout_create_ms
bind_group_create_ms
buffer_allocate_ms
buffer_write_ms
command_encoder_create_ms
compute_pass_encode_ms
queue_submit_ms
gpu_dispatch_only_ms
readback_wall_ms
total_wall_ms
```

`gpu_dispatch_only_ms` must use GPU timestamp query when available. CPU wall-clock timing may be used only for setup components. Do not mix CPU setup timing with GPU dispatch timing into a production promotion verdict.

## Setup Overhead Classes

G211C3R4D must classify setup overhead into exactly one class.

```text
SETUP_OVERHEAD_DOMINANT
BIND_GROUP_OVERHEAD_DOMINANT
PIPELINE_CREATE_OVERHEAD_DOMINANT
BUFFER_ALLOCATION_OVERHEAD_DOMINANT
COMMAND_ENCODER_OVERHEAD_DOMINANT
SETUP_OVERHEAD_NOT_DOMINANT
KERNEL_OR_TILE_LOSS_CONFIRMED_AFTER_SETUP_SPLIT
TIMESTAMP_UNSTABLE_INCONCLUSIVE
PARITY_FAILED
INCONCLUSIVE
```

## Verdict Values

G211C3R4D must produce exactly one setup split verdict.

```text
SETUP_SPLIT_CAPTURED
SETUP_OVERHEAD_DOMINANT
SETUP_OVERHEAD_NOT_DOMINANT
KERNEL_OR_TILE_LOSS_CONFIRMED_AFTER_SETUP_SPLIT
SETUP_TIMESTAMP_UNSTABLE
SETUP_PARITY_FAILED
SETUP_MATRIX_INCOMPLETE
INCONCLUSIVE
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r4d` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_SETUP_OVERHEAD_ISOLATION_PROBE.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_PIPELINE_BIND_GROUP_REUSE_MATRIX.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_SETUP_COMPONENT_SPLIT.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_REUSE_RECOVERY_SUMMARY.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_NEXT_ENTRY_PACKET_G211C3R4E.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_BAKE_MANIFEST.json
artifacts/g211c3r4d/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4D.txt
```

Forbidden output:

```text
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_NEXT_ENTRY_PACKET_G211C4.json
```

## Main Receipt Required Fields

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-70K-G211C3R4D",
  "patch_name": "Pipeline And Bind Group Reuse Split",
  "status": "PASS_ASH_BASETRAIN_GPU_70K_G211C3R4D_SETUP_OVERHEAD_ISOLATION_PROBE",
  "predecessor": "ASH-BASETRAIN-GPU-70K-G211C3R4C",
  "g211c3r4c_entry_verified": true,
  "g211c3_microbench_verdict": "STOP_PERF_LOSS",
  "timestamp_query_status": "TIMESTAMP_QUERY_AVAILABLE",
  "batch_timing_verdict_from_r4c": "SMALL_SHAPE_KERNEL_OR_TILE_LOSS_REMAINS",
  "small_shape_amortization_class_from_r4c": "KERNEL_OR_TILE_LOSS_REMAINS",
  "setup_split_verdict": "SETUP_SPLIT_CAPTURED",
  "setup_overhead_class": "INCONCLUSIVE",
  "promotion_stop_retained": true,
  "runtime_splice_allowed": false,
  "promotion_allowed": false,
  "g211c4_entry_generated": false
}
```

## Next Gate

G211C3R4D routes to G211C3R4E, not G211C4.

```text
ASH-BASETRAIN-GPU-70K-G211C3R4E
Kernel Tile Padding Attribution /
Odd Shape And Tile Utilization Probe /
No Runtime Splice No Promotion Reopen
```

## PASS Criteria

```text
PASS-01 G211C3R4C PASS marker found
PASS-02 G211C3R4C next entry packet found
PASS-03 timestamp_query_status = TIMESTAMP_QUERY_AVAILABLE
PASS-04 batch_timing_verdict = SMALL_SHAPE_KERNEL_OR_TILE_LOSS_REMAINS
PASS-05 G211C3 STOP_PERF_LOSS retained
PASS-06 G211C4 entry packet absent
PASS-07 required setup probe shapes B0/B1 present
PASS-08 pipeline cold/warm split recorded
PASS-09 bind group create/reuse split recorded
PASS-10 buffer allocation/reuse split recorded
PASS-11 command encoder split recorded
PASS-12 GPU dispatch-only timestamp timing retained
PASS-13 setup component split written
PASS-14 reuse recovery summary written
PASS-15 timestamp stability audit written
PASS-16 parity remains pass
PASS-17 setup split verdict selected exactly once
PASS-18 setup overhead class selected exactly once
PASS-19 promotion stop retained
PASS-20 runtime_splice_allowed=false
PASS-21 promotion_allowed=false
PASS-22 G211C3R4E entry packet generated
PASS-23 G211C4 entry packet not generated
PASS-24 forbidden mutation seal passed
PASS-25 PASS marker printed
```

## BLOCKED Codes

```text
ERR_70K_G211C3R4D_G211C3R4C_PASS_MARKER_MISSING
ERR_70K_G211C3R4D_G211C3R4C_ENTRY_PACKET_MISSING
ERR_70K_G211C3R4D_R4C_BATCH_VERDICT_MISMATCH
ERR_70K_G211C3R4D_TIMESTAMP_NOT_AVAILABLE
ERR_70K_G211C3R4D_REQUIRED_SETUP_SHAPE_MISSING
ERR_70K_G211C3R4D_SETUP_TIMESTAMP_UNSTABLE
ERR_70K_G211C3R4D_PARITY_FAILED
ERR_70K_G211C3R4D_UNEXPECTED_G211C4_ENTRY_PACKET
ERR_70K_G211C3R4D_RUNTIME_MUTATION_DETECTED
```

## PASS Meaning

PASS means G211C3R4D captured or explicitly audited pipeline, bind group, buffer, and command encoder setup overhead against GPU timestamp dispatch-only timing.

PASS does not mean TensorCube is faster. PASS does not mean TensorCube timing hygiene is fully repaired. PASS does not mean TensorCube optimization has been applied. PASS does not mean TensorCube promotion is reopened. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean production acceleration exists. PASS does not mean TensorCore is used.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4D setup overhead isolation probe

- Add pipeline and bind group reuse split gate
- Require G211C3R4C small-shape batch timing as entry authority
- Split cold pipeline, bind group create, buffer allocation, command encoder, and hot dispatch paths
- Preserve GPU timestamp dispatch-only timing as dispatch authority
- Compute setup dominance and reuse recovery metrics
- Classify setup overhead versus remaining kernel or tile loss
- Preserve G211C3 STOP_PERF_LOSS and promotion stop
- Route to G211C3R4E kernel tile padding attribution when required
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
