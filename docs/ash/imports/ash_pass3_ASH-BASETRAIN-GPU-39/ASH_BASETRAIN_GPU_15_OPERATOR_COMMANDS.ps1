param([string]$RepoRoot = "D:\1111113232\DUST\1\ash_pass3")
Set-Location $RepoRoot
$env:CARGO_BUILD_JOBS="1"
$env:CARGO_INCREMENTAL="0"
$env:RUSTFLAGS="-C debuginfo=0"
cargo build -p base_train --bin ash_basetrain_gpu_15_chunk_window_logits_expansion_readiness_gate --jobs 1
cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_15_chunk_window_logits_expansion_readiness_gate
