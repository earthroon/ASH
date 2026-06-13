cd "D:\1111113232\DUST\1\ash_pass3"

$env:CARGO_BUILD_JOBS="1"
$env:CARGO_INCREMENTAL="0"
$env:RUSTFLAGS="-C debuginfo=0"

$env:ASH_BASETRAIN_GPU_21_RAW_LOGITS_2048_F32_LE_PATH="D:\1111113232\DUST\1\ash_pass3\target\ash_basetrain_gpu_21_raw_2048_logits.f32le.bin"

cargo build -p base_train --bin ash_basetrain_gpu_23_loss_repeatability_audit --jobs 1 2>&1 | Tee-Object -FilePath ".\target\ash_23_cargo_build.log"
cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_23_loss_repeatability_audit 2>&1 | Tee-Object -FilePath ".\target\ash_basetrain_gpu_23_loss_repeatability_audit.log"
