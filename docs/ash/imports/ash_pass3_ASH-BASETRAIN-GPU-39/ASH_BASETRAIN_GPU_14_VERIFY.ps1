param(
  [string]$RepoRoot = "D:\1111113232\DUST\1\ash_pass3"
)
$src = Join-Path $RepoRoot "crates\base_train\src\ash_basetrain_gpu_14_chunk_window_logits_stability_promotion_gate.rs"
$bin = Join-Path $RepoRoot "crates\base_train\src\bin\ash_basetrain_gpu_14_chunk_window_logits_stability_promotion_gate.rs"
if (!(Test-Path $src)) { throw "missing source: $src" }
if (!(Test-Path $bin)) { throw "missing bin: $bin" }
Write-Host "ASH-BASETRAIN-GPU-14 overlay verify OK"
