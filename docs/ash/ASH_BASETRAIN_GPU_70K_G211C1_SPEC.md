# ASH-BASETRAIN-GPU-70K-G211C1

## Native WGPU Smoke Dispatch Readback / TensorCube 8x8 Reference Kernel Physical Execute / Readback Hash CPU Parity Seal

Seal: Physical Dispatch Evidence Only / No Runtime Route Mutation / No Promotion.

## SSOT

`70K-G211C1` consumes the G211C0 dispatch receipt truth reclassification output as its only entry authority.

`70K-G211C1` may only pass after a native WGPU TensorCube 8x8 reference smoke dispatch physically executes, the output buffer is read back, and the GPU output is compared against a CPU reference under the declared threshold.

`70K-G211C1` must not mutate the TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not write or modify model weights, must not write checkpoints, must not execute a training step, must not replace decode output, and must not claim speedup, translation quality, TensorCore usage, or production readiness.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C0
Dispatch Receipt Truth Reclassification /
G211A3 B10 B17 Physical Dispatch Claim Split /
No Silent Performed Receipt No Promotion
```

Required predecessor evidence:

```text
artifacts/g211c0/ASH_BASETRAIN_GPU_70K_G211C0_NEXT_ENTRY_PACKET_G211C1.json
artifacts/g211c0/ASH_BASETRAIN_GPU_70K_G211C0_DISPATCH_RECEIPT_RECLASSIFICATION.json
artifacts/g211c0/PASS_ASH_BASETRAIN_GPU_70K_G211C0.txt
```

G211C1 must block if the G211C0 entry packet or PASS marker is missing.

## Purpose

G211C1 exists to produce the first physical TensorCube GPU dispatch evidence after G211C0 lowered the previous Submitted/Performed-style receipts to logical transition records.

G211C1 proves only this:

```text
native WGPU dispatch_workgroups was called
queue.submit was called
GPU output was copied to a readback buffer
readback bytes were mapped
CPU reference and GPU output matched under threshold
```

G211C1 does not promote TensorCube. G211C1 does not establish performance gain. G211C1 does not activate production inference.

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c1_native_wgpu_smoke_dispatch_readback.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c1_native_wgpu_smoke_dispatch_readback
```

Alternative command from `crates/base_train`:

```powershell
cargo run --bin ash_basetrain_gpu_70k_g211c1_native_wgpu_smoke_dispatch_readback
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C1_NATIVE_WGPU_SMOKE_DISPATCH_READBACK
```

## TensorCube 8x8 Smoke Contract

G211C1 uses the existing TensorCube 8x8 reference native smoke path from `burn_webgpu_backend`.

Required shape:

```text
M = 8
N = 8
K = 8
A shape = 8x8
B shape = 8x8
C shape = 8x8
dtype = f32
workgroups = [1, 1, 1]
```

Required physical execution steps:

```text
WGPU-01 adapter request
WGPU-02 device/queue request
WGPU-03 shader module creation
WGPU-04 input/output/readback buffer creation
WGPU-05 bind group and compute pipeline creation
WGPU-06 command encoder creation
WGPU-07 compute pass begin
WGPU-08 dispatch_workgroups(1, 1, 1)
WGPU-09 output buffer copy to readback buffer
WGPU-10 queue.submit
WGPU-11 device poll / completion wait
WGPU-12 readback buffer map_async
WGPU-13 CPU reference comparison
```

Missing any physical execution step blocks PASS.

## Local Outputs

The baked package must not contain prebaked `artifacts/g211c1` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c1/ASH_BASETRAIN_GPU_70K_G211C1_NATIVE_WGPU_SMOKE_DISPATCH_READBACK.json
artifacts/g211c1/ASH_BASETRAIN_GPU_70K_G211C1_GPU_READBACK_PARITY_RECEIPT.json
artifacts/g211c1/ASH_BASETRAIN_GPU_70K_G211C1_ADAPTER_FINGERPRINT.json
artifacts/g211c1/ASH_BASETRAIN_GPU_70K_G211C1_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c1/ASH_BASETRAIN_GPU_70K_G211C1_NEXT_ENTRY_PACKET_G211C2.json
artifacts/g211c1/ASH_BASETRAIN_GPU_70K_G211C1_LOCAL_BAKE_VALIDATION.json
artifacts/g211c1/ASH_BASETRAIN_GPU_70K_G211C1_BAKE_MANIFEST.json
artifacts/g211c1/PASS_ASH_BASETRAIN_GPU_70K_G211C1.txt
```

## Required Receipt Fields

Main dispatch receipt:

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-70K-G211C1",
  "patch_name": "Native WGPU Smoke Dispatch Readback",
  "status": "PASS_ASH_BASETRAIN_GPU_70K_G211C1_NATIVE_WGPU_SMOKE_DISPATCH_READBACK",
  "predecessor": "ASH-BASETRAIN-GPU-70K-G211C0",
  "physical_dispatch_executed": true,
  "logical_gate_transition_only": false,
  "shape": { "m": 8, "n": 8, "k": 8, "dtype": "f32" },
  "dispatch": {
    "workgroups": [1, 1, 1],
    "dispatch_workgroups_called": true,
    "queue_submit_called": true,
    "queue_submit_completed": true,
    "readback_performed": true
  },
  "hashes": {
    "input_a_hash": "sha256",
    "input_b_hash": "sha256",
    "cpu_reference_hash": "sha256",
    "gpu_readback_hash": "sha256",
    "shader_source_hash": "sha256"
  },
  "parity": {
    "max_abs_error": 0.0,
    "max_rel_error": 0.0,
    "parity_pass": true
  },
  "forbidden_mutations": {
    "runtime_route_changed": false,
    "tensorcube_runtime_splice_changed": false,
    "production_route_changed": false,
    "weights_changed": false,
    "checkpoint_written": false,
    "optimizer_step_executed": false
  },
  "claims": {
    "quality_claim_allowed": false,
    "speedup_claim_allowed": false,
    "tensorcore_claim_allowed": false,
    "production_promotion_claim_allowed": false
  }
}
```

## Parity Threshold

Default f32 threshold:

```text
max_abs_error <= 0.0001
max_rel_error <= 0.0001
```

The local Rust gate must fail if the native workgroup smoke output does not pass parity against the CPU reference.

## Invariants

```text
physical_dispatch_executed = true
logical_gate_transition_only = false
dispatch_workgroups_called = true
queue_submit_called = true
readback_performed = true
cpu_reference_hash exists
gpu_readback_hash exists
shader_source_hash exists
parity_pass = true
production_route_changed = false
tensorcube_runtime_splice_changed = false
weights_changed = false
checkpoint_written = false
quality_claim_allowed = false
speedup_claim_allowed = false
tensorcore_claim_allowed = false
promotion_allowed = false
next_gate = ASH-BASETRAIN-GPU-70K-G211C2
```

## PASS Meaning

PASS means one native WGPU TensorCube 8x8 reference smoke dispatch physically executed, GPU output was read back, and CPU/GPU parity passed under the declared threshold.

PASS does not mean TensorCube production route is connected. PASS does not mean TensorCube acceleration exists. PASS does not mean TensorCube shape-general matmul is complete. PASS does not mean TensorCore is used. PASS does not mean EN to KO quality improved. PASS does not mean RC quality passed.

## BLOCKED Codes

```text
ERR_70K_G211C1_G211C0_ENTRY_PACKET_MISSING
ERR_70K_G211C1_G211C0_PASS_MARKER_MISSING
ERR_70K_G211C1_ADAPTER_REQUEST_FAILED
ERR_70K_G211C1_DEVICE_REQUEST_FAILED
ERR_70K_G211C1_SHADER_COMPILE_FAILED
ERR_70K_G211C1_DISPATCH_NOT_EXECUTED
ERR_70K_G211C1_QUEUE_SUBMIT_NOT_COMPLETED
ERR_70K_G211C1_READBACK_FAILED
ERR_70K_G211C1_PARITY_MISMATCH
ERR_70K_G211C1_RUNTIME_MUTATION_DETECTED
```

## Next Gate

```text
ASH-BASETRAIN-GPU-70K-G211C2
TensorCube CPU/WGPU Parity Shape Sweep /
8x8 Reference To Shape Matrix Guard /
No Runtime Splice No Production Route
```
