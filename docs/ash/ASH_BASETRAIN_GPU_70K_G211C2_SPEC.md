# ASH-BASETRAIN-GPU-70K-G211C2

## TensorCube CPU/WGPU Parity Shape Sweep / 8x8 Reference To Shape Matrix Guard / No Runtime Splice No Production Route

Seal: Shape Parity Evidence Only / No Runtime Splice / No Production Route.

## SSOT

`70K-G211C2` consumes the G211C1 native WGPU smoke dispatch readback output as its only entry authority.

`70K-G211C2` may only pass after all required TensorCube WGPU matmul candidate shapes physically execute, read back GPU output, and pass CPU/WGPU parity under the declared threshold.

`70K-G211C2` must not mutate the TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not claim speedup, translation quality, TensorCore usage, or production readiness.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C1
Native WGPU Smoke Dispatch Readback /
TensorCube 8x8 Reference Kernel Physical Execute /
Readback Hash CPU Parity Seal
```

Required predecessor evidence:

```text
artifacts/g211c1/ASH_BASETRAIN_GPU_70K_G211C1_NATIVE_WGPU_SMOKE_DISPATCH_READBACK.json
artifacts/g211c1/ASH_BASETRAIN_GPU_70K_G211C1_GPU_READBACK_PARITY_RECEIPT.json
artifacts/g211c1/ASH_BASETRAIN_GPU_70K_G211C1_ADAPTER_FINGERPRINT.json
artifacts/g211c1/ASH_BASETRAIN_GPU_70K_G211C1_NEXT_ENTRY_PACKET_G211C2.json
artifacts/g211c1/PASS_ASH_BASETRAIN_GPU_70K_G211C1.txt
```

G211C2 must block if the G211C1 entry packet or PASS marker is missing.

## Purpose

G211C2 exists to extend the single 8x8 G211C1 physical dispatch proof into a bounded CPU/WGPU parity shape sweep.

G211C2 proves only this:

```text
required shapes S0-S5 physically dispatched
queue.submit was called for every required shape
GPU output was read back for every required shape
CPU reference and GPU output matched for every required shape
odd-shape edge guard did not expose padding, indexing, or K-loop errors
```

G211C2 does not promote TensorCube. G211C2 does not establish performance gain. G211C2 does not activate production inference.

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c2_tensorcube_parity_shape_sweep.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c2_tensorcube_parity_shape_sweep
```

Alternative command from `crates/base_train`:

```powershell
cargo run --bin ash_basetrain_gpu_70k_g211c2_tensorcube_parity_shape_sweep
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C2_TENSORCUBE_PARITY_SHAPE_SWEEP
```

## Required Shape Sweep

```text
S0 = [8, 8, 8]
S1 = [16, 16, 8]
S2 = [16, 16, 64]
S3 = [64, 64, 64]
S4 = [128, 128, 128]
S5 = [17, 31, 65]
```

Shape meaning:

```text
A shape = M x K
B shape = K x N
C shape = M x N
dtype = f32
layout = row_major
```

CPU reference:

```text
C[row, col] = sum(A[row, k] * B[k, col] for k in 0..K)
```

## Deterministic Input Pattern

```text
A[row, col] = ((row * K + col + 1) % 251) / 251.0
B[row, col] = (((row + 3) * (col + 5)) % 257) / 257.0
```

The input pattern must prevent zero-output false pass, identity-only false pass, row/column indexing false pass, transposed-B false pass, K-loop omission, and odd-shape padding leakage.

## WGPU Execution Contract

For every required shape, G211C2 must execute:

```text
WGPU-01 adapter/device/queue prepared
WGPU-02 shape-specific input buffers created
WGPU-03 shape-specific output buffer created
WGPU-04 shape-specific readback buffer created
WGPU-05 shader module created or reused
WGPU-06 bind group created
WGPU-07 compute pipeline created or reused
WGPU-08 command encoder created
WGPU-09 compute pass begun
WGPU-10 dispatch_workgroups called
WGPU-11 output buffer copied to readback buffer
WGPU-12 queue.submit called
WGPU-13 device poll / completion wait
WGPU-14 readback buffer map_async
WGPU-15 GPU output bytes decoded
WGPU-16 CPU reference compared
WGPU-17 shape parity receipt recorded
```

Any missing required physical execution step blocks PASS for that shape. Any required shape failure blocks G211C2 PASS.

## Dispatch Grid Contract

```text
tile_m = 8
tile_n = 8
workgroups_x = ceil_div(N, tile_n)
workgroups_y = ceil_div(M, tile_m)
workgroups_z = 1
```

## Parity Threshold

Default f32 threshold:

```text
max_abs_error <= 0.0001
max_rel_error <= 0.0001
mean_abs_error <= 0.00001
```

If an internal f16 path is used, it must be explicitly recorded. The default G211C2 target is f32.

## Local Outputs

The baked package must not contain prebaked `artifacts/g211c2` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c2/ASH_BASETRAIN_GPU_70K_G211C2_TENSORCUBE_PARITY_SHAPE_SWEEP.json
artifacts/g211c2/ASH_BASETRAIN_GPU_70K_G211C2_SHAPE_PARITY_MATRIX.json
artifacts/g211c2/ASH_BASETRAIN_GPU_70K_G211C2_ADAPTER_FINGERPRINT.json
artifacts/g211c2/ASH_BASETRAIN_GPU_70K_G211C2_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c2/ASH_BASETRAIN_GPU_70K_G211C2_NEXT_ENTRY_PACKET_G211C3.json
artifacts/g211c2/ASH_BASETRAIN_GPU_70K_G211C2_LOCAL_BAKE_VALIDATION.json
artifacts/g211c2/ASH_BASETRAIN_GPU_70K_G211C2_BAKE_MANIFEST.json
artifacts/g211c2/PASS_ASH_BASETRAIN_GPU_70K_G211C2.txt
```

## Required Receipt Fields

Main sweep receipt must include:

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-70K-G211C2",
  "patch_name": "TensorCube CPU/WGPU Parity Shape Sweep",
  "status": "PASS_ASH_BASETRAIN_GPU_70K_G211C2_TENSORCUBE_PARITY_SHAPE_SWEEP",
  "predecessor": "ASH-BASETRAIN-GPU-70K-G211C1",
  "g211c1_entry_verified": true,
  "physical_dispatch_executed": true,
  "logical_gate_transition_only": false,
  "sweep": {
    "shape_count": 6,
    "required_shape_count": 6,
    "all_required_shapes_executed": true,
    "all_required_shapes_passed": true
  },
  "parity_summary": {
    "max_abs_error_global": 0.0,
    "max_rel_error_global": 0.0,
    "mean_abs_error_global": 0.0,
    "parity_pass": true
  },
  "forbidden_mutations": {
    "runtime_route_changed": false,
    "tensorcube_runtime_splice_changed": false,
    "production_route_changed": false,
    "decode_output_replaced": false,
    "weights_changed": false,
    "checkpoint_written": false,
    "optimizer_step_executed": false,
    "training_step_executed": false
  },
  "claims": {
    "quality_claim_allowed": false,
    "speedup_claim_allowed": false,
    "tensorcore_claim_allowed": false,
    "production_promotion_claim_allowed": false
  }
}
```

## Shape Parity Matrix

The matrix must contain all shape IDs:

```text
S0, S1, S2, S3, S4, S5
```

Each shape entry must contain:

```text
shape_id
shape { m, n, k }
dtype
dtype_internal
input_a_hash
input_b_hash
cpu_reference_hash
gpu_readback_hash
workgroups_x
workgroups_y
workgroups_z
dispatch_workgroups_called
queue_submit_called
queue_submit_completed
readback_performed
max_abs_error
max_rel_error
mean_abs_error
parity_pass
```

## Invariants

```text
physical_dispatch_executed = true
logical_gate_transition_only = false
all_required_shapes_executed = true
all_required_shapes_passed = true
dispatch_workgroups_called = true for every shape
queue_submit_called = true for every shape
readback_performed = true for every shape
cpu_reference_hash exists for every shape
gpu_readback_hash exists for every shape
shader_source_hash exists
parity_pass = true for every shape
production_route_changed = false
tensorcube_runtime_splice_changed = false
runtime_splice_allowed = false
weights_changed = false
checkpoint_written = false
quality_claim_allowed = false
speedup_claim_allowed = false
tensorcore_claim_allowed = false
promotion_allowed = false
next_gate = ASH-BASETRAIN-GPU-70K-G211C3
```

## PASS Meaning

PASS means TensorCube WGPU matmul candidate shape sweep physically executed, read back GPU outputs, and verified CPU/WGPU parity for all required shapes under the declared threshold.

PASS does not mean TensorCube production route is connected. PASS does not mean TensorCube runtime splice is active. PASS does not mean TensorCube acceleration exists. PASS does not mean TensorCube beats burn/cubecl matmul. PASS does not mean TensorCore is used. PASS does not mean EN to KO quality improved.

## BLOCKED Codes

```text
ERR_70K_G211C2_G211C1_ENTRY_PACKET_MISSING
ERR_70K_G211C2_G211C1_PASS_MARKER_MISSING
ERR_70K_G211C2_ADAPTER_REQUEST_FAILED
ERR_70K_G211C2_DEVICE_REQUEST_FAILED
ERR_70K_G211C2_SHADER_COMPILE_FAILED
ERR_70K_G211C2_REQUIRED_SHAPE_NOT_EXECUTED
ERR_70K_G211C2_DISPATCH_NOT_CALLED
ERR_70K_G211C2_QUEUE_SUBMIT_NOT_CALLED
ERR_70K_G211C2_READBACK_FAILED
ERR_70K_G211C2_PARITY_MISMATCH
ERR_70K_G211C2_EDGE_SHAPE_PADDING_ERROR
ERR_70K_G211C2_RUNTIME_MUTATION_DETECTED
```

## Next Gate

```text
ASH-BASETRAIN-GPU-70K-G211C3
TensorCube Microbench Baseline /
Burn Matmul Versus TensorCube Candidate /
Perf Win Required For Further Promotion
```
