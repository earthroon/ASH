param(
  [string]$RepoRoot = "D:\1111113232\DUST\1\ash_pass3"
)
$ErrorActionPreference = "Stop"
$lib = Join-Path $RepoRoot "crates\base_train\src\lib.rs"
$module = Join-Path $RepoRoot "crates\base_train\src\ash_basetrain_gpu_05r1_atlas_group_forward_candidate_readiness_reaudit.rs"
$bin = Join-Path $RepoRoot "crates\base_train\src\bin\ash_basetrain_gpu_05r1_atlas_group_forward_candidate_readiness_reaudit.rs"
if (!(Test-Path $lib)) { throw "missing lib.rs" }
if (!(Test-Path $module)) { throw "missing 05R1 module" }
if (!(Test-Path $bin)) { throw "missing 05R1 bin" }
$libText = Get-Content $lib -Raw
if ($libText -notmatch 'pub\s+mod\s+ash_basetrain_gpu_05r1_atlas_group_forward_candidate_readiness_reaudit\s*;') {
  throw "05R1 pub mod export missing from lib.rs"
}
$binText = Get-Content $bin -Raw
if ($binText -notmatch 'base_train::ash_basetrain_gpu_05r1_atlas_group_forward_candidate_readiness_reaudit') {
  throw "05R1 bin import does not target exported module"
}
Write-Host "PASS_ASH_BASETRAIN_GPU_05R1_R1_LIB_EXPORT_BIND_VERIFY"
