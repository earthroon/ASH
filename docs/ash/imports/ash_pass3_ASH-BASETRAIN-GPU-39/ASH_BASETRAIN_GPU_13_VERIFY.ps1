param(
  [string]$RepoRoot = "D:\1111113232\DUST\1\ash_pass3"
)
$src = Join-Path $RepoRoot "crates\base_train\src\ash_basetrain_gpu_13_chunk_window_logits_value_stability_audit.rs"
$bin = Join-Path $RepoRoot "crates\base_train\src\bin\ash_basetrain_gpu_13_chunk_window_logits_value_stability_audit.rs"
if (!(Test-Path $src)) { throw "missing ASH-BASETRAIN-GPU-13 source" }
if (!(Test-Path $bin)) { throw "missing ASH-BASETRAIN-GPU-13 bin" }
Write-Host "ASH-BASETRAIN-GPU-13 verify OK."
