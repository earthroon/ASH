# SFT-GPU-RUN-10 이후 로드맵

## Current SSOT

`SFT-GPU-RUN-10` is now the latest baked seal over `SFT-GPU-RUN-09`.

Current state:

```txt
strict GPU train → artifact intake → regression matrix → promotion bridge → operator approval → runtime attach dry-run → promotion apply candidate → current pointer switch → post-switch health → rollback drill simulation
```

## RUN-11 — GPU-Trained Slot Arbitration / Multi-Adapter Health Merge Seal

Purpose:

- Merge the GPU-trained current adapter into slot-level arbitration.
- Compare post-switch health, rollback drill readiness, fallback readiness, demotion readiness, and quarantine readiness.
- Generate recommendations only.

Must remain closed:

- actual current pointer switch
- demotion apply
- quarantine apply
- rollback execution
- lifecycle mutation
- ASH binding

## RUN-12 — GPU-Trained Lifecycle Ledger Merge / Training Lineage Seal

Purpose:

- Append strict GPU train lineage, artifact intake, regression matrix, approval, current switch, post-switch health, and rollback drill into lifecycle ledger.
- Append-only only.

Must remain closed:

- silent lifecycle mutation
- current pointer update
- unreviewed state transition
- demotion/quarantine apply

## RUN-13 — GPU-Trained Operator Action Apply / Lifecycle Transition Seal

Purpose:

- Apply only operator-reviewed actions that match RUN-11 recommendation and RUN-12 lifecycle lineage.
- This is where reviewed fallback/demotion/quarantine/candidate switch can finally open.

Must reject:

- unreviewed action apply
- recommendation mismatch apply
- silent registry correction
- runtime SFT training / gradient / optimizer

## Parallel hardening

- SFT-GPU-SAFETY-01 — GPU Train OOM / Timeout / Device Lost Recovery Seal
- SFT-GPU-SAFETY-02 — Partial Artifact Quarantine / Failed Train Output Guard
- SFT-GPU-OBS-01 — Strict GPU Train Telemetry Dashboard / Matrix Drift Console Seal
- SFT-GPU-OBS-02 — Long-Horizon GPU Adapter Health Ledger / Runtime Drift Seal
