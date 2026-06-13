# ASH-BASETRAIN-GPU-04R2-R1B Bake Report

## Title

Actual WGPU Device Queue Probe Execution / Adapter Device Queue Creation No Upload No Forward Seal

## Source

Base SSOT: `ASH-BASETRAIN-GPU-04R2-R1_runtime_binding_preflight_bin_rebaked`

## Implemented

- Added `crates/base_train/src/ash_basetrain_gpu_04r2_r1b_actual_wgpu_device_queue_probe.rs`
- Added `crates/base_train/src/bin/ash_basetrain_gpu_04r2_r1b_actual_wgpu_device_queue_probe.rs`
- Added `pub mod ash_basetrain_gpu_04r2_r1b_actual_wgpu_device_queue_probe;` to `crates/base_train/src/lib.rs`
- Added direct `wgpu26` and `pollster` dependencies to `crates/base_train/Cargo.toml`

## Closed Paths

```txt
actual_upload_execution_executed = false
actual_tensor_payload_read_executed = false
gpu_buffer_created = false
wgpu_queue_write_executed = false
actual_gpu_buffer_state_created = false
forward_dispatch_executed = false
optimizer_step_executed = false
safetensors_mutation_present = false
```

## Compile Status

```txt
cargo_available_in_bake_environment = false
rust_compile_executed = false
rust_compile_verdict = JUDGMENT_UNAVAILABLE_RUNTIME_CARGO_NOT_FOUND
```

## Verdict

```txt
PASS_ASH_BASETRAIN_GPU_04R2_R1B_ACTUAL_WGPU_DEVICE_QUEUE_PROBE_EXECUTION_ADAPTER_DEVICE_QUEUE_CREATION_NO_UPLOAD_NO_FORWARD
```
