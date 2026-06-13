cd "D:\1111113232\DUST\1\ash_pass3"

$env:CARGO_BUILD_JOBS="1"
$env:CARGO_INCREMENTAL="0"
$env:RUSTFLAGS="-C debuginfo=0"

cargo build -p base_train --bin ash_basetrain_gpu_21_0_raw_logits_payload_export --jobs 1 2>&1 | Tee-Object -FilePath ".\target\ash_21_0_cargo_build.log"

$env:ASH_BASETRAIN_EXTERNAL_SHARD_FILE="D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts\ash_v5_native_genesis.forge01_smoke.safetensors"
$env:ASH_BASETRAIN_EXTERNAL_SHARD_ROOT="D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts"
$env:ASH_BASETRAIN_WGPU_BACKEND="auto"
$env:ASH_BASETRAIN_DEVICE_POLICY="prefer_discrete"
$env:ASH_BASETRAIN_GPU_21_RAW_LOGITS_2048_F32_LE_EXPORT_PATH="D:\1111113232\DUST\1\ash_pass3\target\ash_basetrain_gpu_21_raw_2048_logits.f32le.bin"

cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_21_0_raw_logits_payload_export 2>&1 | Tee-Object -FilePath ".\target\ash_basetrain_gpu_21_0_raw_logits_payload_export.log"

$env:ASH_BASETRAIN_GPU_21_RAW_LOGITS_2048_F32_LE_PATH="D:\1111113232\DUST\1\ash_pass3\target\ash_basetrain_gpu_21_raw_2048_logits.f32le.bin"

cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_21_local_window_loss_smoke 2>&1 | Tee-Object -FilePath ".\target\ash_basetrain_gpu_21_local_window_loss_smoke_after_21_0.log"
