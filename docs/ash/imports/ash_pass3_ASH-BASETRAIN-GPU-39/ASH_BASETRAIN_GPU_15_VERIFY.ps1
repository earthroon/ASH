param([string]$RepoRoot = "D:\1111113232\DUST\1\ash_pass3")
$src = Join-Path $RepoRoot "crates\base_train\src\ash_basetrain_gpu_15_chunk_window_logits_expansion_readiness_gate.rs"
$bin = Join-Path $RepoRoot "crates\base_train\src\bin\ash_basetrain_gpu_15_chunk_window_logits_expansion_readiness_gate.rs"
if (!(Test-Path $src)) { throw "missing ASH-BASETRAIN-GPU-15 source" }
if (!(Test-Path $bin)) { throw "missing ASH-BASETRAIN-GPU-15 bin" }
Write-Host "ASH-BASETRAIN-GPU-15 overlay verified"
