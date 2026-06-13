param([string]$RepoRoot = "D:\1111113232\DUST\1\ash_pass3")
$src = Join-Path $RepoRoot "crates\base_train\src\ash_basetrain_gpu_16_chunk_window_logits_expansion_dispatch_smoke.rs"
$bin = Join-Path $RepoRoot "crates\base_train\src\bin\ash_basetrain_gpu_16_chunk_window_logits_expansion_dispatch_smoke.rs"
if (!(Test-Path $src)) { throw "missing source: $src" }
if (!(Test-Path $bin)) { throw "missing bin: $bin" }
$content = Get-Content $bin -Raw
if ($content -notmatch "#\[path = \"\.\./ash_basetrain_gpu_16_chunk_window_logits_expansion_dispatch_smoke\.rs\"\]") { throw "direct bin rebind missing" }
Write-Host "ASH-BASETRAIN-GPU-16 verify OK."
