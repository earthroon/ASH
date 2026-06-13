param(
  [string]$RepoRoot = "D:\1111113232\DUST\1\ash_pass3"
)
$ErrorActionPreference = "Stop"
$PacketRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$OverlayRoot = Join-Path $PacketRoot "overlay"
$Targets = @(
  "crates\base_train\src\lib.rs",
  "crates\base_train\src\ash_basetrain_gpu_05r1_atlas_group_forward_candidate_readiness_reaudit.rs",
  "crates\base_train\src\bin\ash_basetrain_gpu_05r1_atlas_group_forward_candidate_readiness_reaudit.rs"
)
foreach ($rel in $Targets) {
  $src = Join-Path $OverlayRoot $rel
  $dst = Join-Path $RepoRoot $rel
  if (!(Test-Path $src)) { throw "missing overlay source: $src" }
  if (Test-Path $dst) {
    Copy-Item $dst "$dst.ash_05r1_r1.bak" -Force
  }
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dst) | Out-Null
  Copy-Item $src $dst -Force
  Write-Host "overlaid $rel"
}
