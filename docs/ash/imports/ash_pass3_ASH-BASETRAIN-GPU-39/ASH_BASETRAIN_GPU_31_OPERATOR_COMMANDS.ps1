cd "D:\1111113232\DUST\1\ash_pass3"

$env:CARGO_BUILD_JOBS="1"
$env:CARGO_INCREMENTAL="0"
$env:RUSTFLAGS="-C debuginfo=0"

# Primary input produced or materialized from ASH-BASETRAIN-GPU-30 when available.
$env:ASH_BASETRAIN_GPU_30_CPU_LOGITS_GRADIENT_CANDIDATE_F32_LE_PATH="D:\1111113232\DUST\1\ash_pass3\target\ash_basetrain_gpu_30_cpu_logits_gradient_candidate.f32le.bin"

# Fallback input: if the CPU candidate file is absent, ASH-BASETRAIN-GPU-31 recomputes from raw logits
# only when the raw payload digest matches the ASH-BASETRAIN-GPU-26/30 receipt.
$env:ASH_BASETRAIN_GPU_21_RAW_LOGITS_2048_F32_LE_PATH="D:\1111113232\DUST\1\ash_pass3\target\ash_basetrain_gpu_21_raw_2048_logits.f32le.bin"

cargo build -p base_train --bin ash_basetrain_gpu_31_gpu_logits_gradient_write_smoke --jobs 1 2>&1 | Tee-Object -FilePath ".\target\ash_31_cargo_build.log"

cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_31_gpu_logits_gradient_write_smoke 2>&1 | Tee-Object -FilePath ".\target\ash_basetrain_gpu_31_gpu_logits_gradient_write_smoke.log"
