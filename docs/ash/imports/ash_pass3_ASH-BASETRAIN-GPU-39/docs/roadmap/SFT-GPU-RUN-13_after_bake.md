# After SFT-GPU-RUN-13 Roadmap

## Current SSOT

SFT-GPU-RUN-13 opens only operator-reviewed lifecycle action apply. RUN-11 recommendation, RUN-12 lifecycle lineage, and operator review receipt must align before any action receipt or lifecycle transition event is emitted.

## Closed After RUN-13

- unreviewed action apply
- recommendation mismatch apply
- silent registry correction
- runtime SFT training
- runtime gradient write
- runtime optimizer step
- textureSample/sampler/normalized UV weight fetch
- CPU fallback as success

## Natural Next Steps

### SFT-GPU-SAFETY-01 — GPU Train OOM / Timeout / Device Lost Recovery Seal
Add explicit failed-state receipts for GPU train/runtime validation failures without CPU fallback success.

### SFT-GPU-SAFETY-02 — Partial Artifact Quarantine / Failed Train Output Guard
Block zero-byte, partial, interrupted, or failed-parity adapter artifacts from registry intake and promotion paths.

### SFT-GPU-OBS-01 — Strict GPU Train Telemetry Dashboard / Matrix Drift Console Seal
Expose train/promotion/post-switch/operator-apply telemetry as a long-running observation console.

### SFT-GPU-OBS-02 — Long-Horizon GPU Adapter Health Ledger / Runtime Drift Seal
Track current GPU-trained adapter health drift after operator-reviewed lifecycle action apply.

### ASH Binding Follow-up Candidate
Only after the RUN-13 operator apply seal is locally compiled and reviewed should ASH current binding finalization be considered.
