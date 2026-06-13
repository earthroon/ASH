cd "D:\1111113232\DUST\1\ash_pass3"

$env:CARGO_BUILD_JOBS="1"
$env:CARGO_INCREMENTAL="0"
$env:RUSTFLAGS="-C debuginfo=0"

cargo build -p base_train --bin ash_basetrain_gpu_28_gradient_buffer_allocation_candidate --jobs 1 2>&1 | Tee-Object -FilePath ".\target\ash_28_cargo_build.log"

cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_28_gradient_buffer_allocation_candidate 2>&1 | Tee-Object -FilePath ".\target\ash_basetrain_gpu_28_gradient_buffer_allocation_candidate.log"
