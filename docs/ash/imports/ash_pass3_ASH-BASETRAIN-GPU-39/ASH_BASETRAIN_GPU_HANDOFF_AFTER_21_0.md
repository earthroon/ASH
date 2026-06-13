# ASH BaseTrain GPU Handoff After 21-0

## Current patch

ASH-BASETRAIN-GPU-21-0 — Raw Logits Payload Export / Window 2048 Readback Bytes Materialization For Local Loss Smoke No Loss No Backward No Optimizer Seal

## Next if PASS

ASH-BASETRAIN-GPU-21-R2 — Local Window Loss Smoke Rerun / Exported Raw Payload To Fixed Target 1 Loss Scalar No Backward No Optimizer Seal

## Next if FAIL

ASH-BASETRAIN-GPU-21-0A — Raw Logits Payload Export Failure Triage / Source Digest Dispatch Readback File Write Or Digest Blocker Detail No Loss No Optimizer Seal

## Required local payload export command

```powershell
cd "D:\1111113232\DUST\1\ash_pass3"

$env:ASH_BASETRAIN_EXTERNAL_SHARD_FILE="D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts\ash_v5_native_genesis.forge01_smoke.safetensors"
$env:ASH_BASETRAIN_EXTERNAL_SHARD_ROOT="D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts"
$env:ASH_BASETRAIN_WGPU_BACKEND="auto"
$env:ASH_BASETRAIN_DEVICE_POLICY="prefer_discrete"
$env:ASH_BASETRAIN_GPU_21_RAW_LOGITS_2048_F32_LE_EXPORT_PATH="D:\1111113232\DUST\1\ash_pass3\target\ash_basetrain_gpu_21_raw_2048_logits.f32le.bin"

cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_21_0_raw_logits_payload_export
```

## Required 21 rerun env

```powershell
$env:ASH_BASETRAIN_GPU_21_RAW_LOGITS_2048_F32_LE_PATH="D:\1111113232\DUST\1\ash_pass3\target\ash_basetrain_gpu_21_raw_2048_logits.f32le.bin"

cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_21_local_window_loss_smoke
```
