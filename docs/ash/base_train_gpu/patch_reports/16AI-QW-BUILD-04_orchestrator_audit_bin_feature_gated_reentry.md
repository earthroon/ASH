# 16AI-QW-BUILD-04 — Orchestrator Audit Bin Feature-gated Reentry / Required Features Seal

## Status
STATIC_PASS_ORCHESTRATOR_AUDIT_BIN_FEATURE_GATED_REENTRY

## SSOT
- Primary: `crates/orchestrator_local/Cargo.toml`
- `autobins = false`
- main bin: `orchestrator_local` / `src/main.rs`
- audit feature: `orchestrator_audit_bins`
- audit bin count: 73
- audit bin sources deleted: false
- script-only bypass used: false

## Implemented
- Disabled automatic `src/bin/*.rs` discovery for `orchestrator_local`.
- Registered the canonical main bin explicitly.
- Registered every existing audit bin with `required-features = ["orchestrator_audit_bins"]`.
- Wrote manifest, summary, receipt, trace, and repair queue artifacts.

## Reentry
Default build should not compile orchestrator audit bins.

```powershell
cargo build
```

Audit reentry remains explicit:

```powershell
cargo build -p orchestrator_local --features orchestrator_audit_bins --bins
```

## Guard
- audit bin deletion: forbidden
- fake API shim: forbidden
- default build contamination: forbidden
- R12A-R1 hidden capture logic modification: forbidden

## Next
After local default build passes, retry:

```powershell
.\scripts\run_16AI_QW_38G_R6A_R12A_R1_trace_capture_expansion.ps1 -Build
```
