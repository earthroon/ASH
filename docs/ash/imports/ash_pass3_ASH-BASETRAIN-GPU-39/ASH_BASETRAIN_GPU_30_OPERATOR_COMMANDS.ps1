cd "D:\1111113232\DUST\1\ash_pass3"

$env:CARGO_BUILD_JOBS="1"
$env:CARGO_INCREMENTAL="0"
$env:RUSTFLAGS="-C debuginfo=0"

# Required source payload from ASH-BASETRAIN-GPU-21-0 / 24 line.
# Adjust only if your local payload file is stored elsewhere.
$env:ASH_BASETRAIN_GPU_21_RAW_LOGITS_2048_F32_LE_PATH="D:\1111113232\DUST\1\ash_pass3\target\ash_basetrain_gpu_21_raw_2048_logits.f32le.bin"

cargo build -p base_train --bin ash_basetrain_gpu_30_cpu_logits_gradient_formula_receipt --jobs 1 2>&1 | Tee-Object -FilePath ".\target\ash_30_cargo_build.log"

cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_30_cpu_logits_gradient_formula_receipt 2>&1 | Tee-Object -FilePath ".\target\ash_basetrain_gpu_30_cpu_logits_gradient_formula_receipt.log"
