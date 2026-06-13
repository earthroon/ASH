param([string]$RepoRoot = "D:\1111113232\DUST\1\ash_pass3")
Set-Location $RepoRoot
$env:CARGO_BUILD_JOBS="1"
$env:CARGO_INCREMENTAL="0"
$env:RUSTFLAGS="-C debuginfo=0"
$env:ASH_BASETRAIN_EXTERNAL_SHARD_FILE="D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts\ash_v5_native_genesis.forge01_smoke.safetensors"
$env:ASH_BASETRAIN_EXTERNAL_SHARD_ROOT="D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts"
$env:ASH_BASETRAIN_WGPU_BACKEND="auto"
$env:ASH_BASETRAIN_DEVICE_POLICY="prefer_discrete"
cargo build -p base_train --bin ash_basetrain_gpu_16_chunk_window_logits_expansion_dispatch_smoke --jobs 1
cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_16_chunk_window_logits_expansion_dispatch_smoke
