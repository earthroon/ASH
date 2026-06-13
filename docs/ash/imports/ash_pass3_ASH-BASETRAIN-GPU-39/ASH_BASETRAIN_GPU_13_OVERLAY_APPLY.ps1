param(
  [string]$RepoRoot = "D:\1111113232\DUST\1\ash_pass3"
)
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -Force "$Here\crates\base_train\src\ash_basetrain_gpu_13_chunk_window_logits_value_stability_audit.rs" "$RepoRoot\crates\base_train\src\ash_basetrain_gpu_13_chunk_window_logits_value_stability_audit.rs"
Copy-Item -Force "$Here\crates\base_train\src\bin\ash_basetrain_gpu_13_chunk_window_logits_value_stability_audit.rs" "$RepoRoot\crates\base_train\src\bin\ash_basetrain_gpu_13_chunk_window_logits_value_stability_audit.rs"
Write-Host "ASH-BASETRAIN-GPU-13 overlay applied."
