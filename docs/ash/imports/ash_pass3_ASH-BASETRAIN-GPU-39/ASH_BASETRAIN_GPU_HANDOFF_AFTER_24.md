# ASH BaseTrain GPU Handoff After 24

Latest baked patch:
ASH-BASETRAIN-GPU-24 GPU Local Loss Candidate / Window 2048 Target 1 Loss Kernel Candidate No Backward No Optimizer Seal

Source SSOT:
ASH-BASETRAIN-GPU-23 PASS receipt.

Runtime command:
```powershell
cd "D:\1111113232\DUST\1\ash_pass3"
$env:CARGO_BUILD_JOBS="1"
$env:CARGO_INCREMENTAL="0"
$env:RUSTFLAGS="-C debuginfo=0"
$env:ASH_BASETRAIN_GPU_21_RAW_LOGITS_2048_F32_LE_PATH="D:\1111113232\DUST\1\ash_pass3\target\ash_basetrain_gpu_21_raw_2048_logits.f32le.bin"
$env:ASH_BASETRAIN_WGPU_BACKEND="auto"
$env:ASH_BASETRAIN_DEVICE_POLICY="prefer_discrete"
cargo build -p base_train --bin ash_basetrain_gpu_24_gpu_local_loss_candidate --jobs 1
cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_24_gpu_local_loss_candidate
```

PASS route:
ASH-BASETRAIN-GPU-25 GPU Local Loss Repeatability Audit / Repeated Window 2048 Target 1 GPU Loss Candidate Stability No Backward No Optimizer Seal

FAIL route:
ASH-BASETRAIN-GPU-24A GPU Local Loss Candidate Failure Triage / Runtime Buffer Dispatch Readback Numeric Or Boundary Blocker Detail No Optimizer Seal
