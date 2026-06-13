param([string]$RepoRoot = "D:\1111113232\DUST\1\ash_pass3")
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -Force (Join-Path $Here "crates\base_train\src\ash_basetrain_gpu_15_chunk_window_logits_expansion_readiness_gate.rs") (Join-Path $RepoRoot "crates\base_train\src\ash_basetrain_gpu_15_chunk_window_logits_expansion_readiness_gate.rs")
Copy-Item -Force (Join-Path $Here "crates\base_train\src\bin\ash_basetrain_gpu_15_chunk_window_logits_expansion_readiness_gate.rs") (Join-Path $RepoRoot "crates\base_train\src\bin\ash_basetrain_gpu_15_chunk_window_logits_expansion_readiness_gate.rs")
