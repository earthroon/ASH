# 16AI-QW-LEGACY-01 Acceptance — Runtime UNZ Legacy Default Build Quarantine

## Required Evidence
- `runtime_unz_legacy_workspace_member = true`
- `runtime_unz_legacy_default_member = false`
- `runtime_unz_legacy_default_build_compiled = false`
- `runtime_unz_legacy_deleted = false`
- `legacy_api_drift_detected = true`
- `legacy_api_drift_repaired = false`
- `script_only_bypass_used = false`

## Expected Local Verification
```powershell
.\scriptsun_16AI_QW_LEGACY_01_runtime_unz_quarantine.ps1 -Build -Metadata
.\scriptsun_16AI_QW_38G_R6A_R12A_R1_trace_capture_expansion.ps1 -Build
```

## Explicit Legacy Build
`cargo build -p runtime_unz_legacy` may still fail until LEGACY-02. That is not a LEGACY-01 failure if default build is unblocked.
