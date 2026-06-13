# SFT-FFN-INFRA-GPU-SAFETY-01 Bake Report

## Base

`ash_pass3_SFT-FFN-LORA-09_runtime_attach_dry_run_baked.zip`

## Added

- `crates/ash_core/src/infra_gpu_safety.rs`
- `crates/ash_core/tests/sft_ffn_infra_gpu_safety_01.rs`
- `crates/burn_webgpu_backend/src/gpu_safety.rs`
- `crates/burn_webgpu_backend/tests/gpu_safety_01_readback_telemetry.rs`
- `acceptance_reports/SFT-FFN-INFRA-GPU-SAFETY-01_wgpu_readback_telemetry_gate.md`
- `bake_artifacts/SFT-FFN-INFRA-GPU-SAFETY-01_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-INFRA-GPU-SAFETY-01_STATIC_VALIDATION.txt`
- `bake_artifacts/SFT-FFN-INFRA-GPU-SAFETY-01_FILE_DIGESTS.sha256`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/model_core/src/gpu_penalty.rs`
- `crates/model_core/src/generation_telemetry.rs`
- `crates/burn_webgpu_backend/Cargo.toml`
- `crates/burn_webgpu_backend/src/gpu_sampling.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- WGPU map_async readback deadlock guard
- explicit device.poll callback progress boundary
- bounded readback timeout guard
- profiling feature for backend us-level telemetry
- model_core telemetry conversion gate

## Closed

- unbounded readback `rx.recv()` in targeted helpers
- per-token telemetry always-on default
- production runtime attach
- promotion apply
- current pointer update
