# SFT-GPU-OBS-02 After-Bake Roadmap

## Current SSOT

```txt
Latest baked line:
SFT-GPU-OBS-02 — Long-Horizon GPU Adapter Health Ledger / Runtime Drift Seal
```

OBS-02 consumes OBS-01 telemetry dashboard snapshots and produces append-only long-horizon health ledger events. It tracks health score trend, smoke pass/fail trend, fallback readiness drift, rollback availability drift, adapter digest drift, runtime backend drift, textureLoad guard drift, fault recovery trend, and partial artifact quarantine trend.

## Still Closed

```txt
current pointer update
operator action apply
fallback activation
rollback execution
demotion apply
quarantine apply
registry mutation
promotion apply
lifecycle mutation
runtime SFT training
runtime gradient write
runtime optimizer step
partial artifact auto-repair
silent CPU fallback success
silent backend switch
silent registry correction
textureSample / sampler / normalized UV weight fetch
```

## Recommended Next Roadmap

### SFT-GPU-OBS-03 — Operator Health Review Console / Long-Horizon Attention Queue Seal

Purpose:
- Convert OBS-02 long-horizon severity and operator_attention_required into review queue entries.
- Keep queue visibility-only unless a later operator action apply patch explicitly opens action handling.

### SFT-GPU-OBS-04 — Drift Threshold Policy Versioning / Tunable Severity Matrix Seal

Purpose:
- Move hard-coded warning/critical thresholds into a policy snapshot.
- Seal policy version with each long-horizon ledger event for reproducible severity decisions.

### SFT-GPU-OBS-05 — Backend Drift Correlation / Device Fault Timeline Seal

Purpose:
- Correlate device lost, backend fingerprint drift, timeout, OOM, and CPU fallback attempts across time.
- Keep correlation observational only.

### SFT-GPU-OBS-06 — Quarantine Pressure Trend / Failed Output Cluster Seal

Purpose:
- Track repeated partial artifact quarantine patterns by train run, adapter slot, and backend fingerprint.
- Use as review signal, not automatic demotion/quarantine apply.

### SFT-GPU-RUN-14 — Reviewed Health-Based Action Candidate Intake Seal

Purpose:
- Read OBS-02/OBS-03 review outputs and prepare action candidates.
- Still require operator receipt before any apply path.

## Local Verification

```bash
cargo test -p ash_core sft_gpu_obs_02 -- --nocapture
cargo test -p lora_train gpu_adapter_health_ledger -- --nocapture
cargo test -p burn_webgpu_backend gpu_runtime_drift_ledger -- --nocapture
```
