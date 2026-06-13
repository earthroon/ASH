# SFT-GPU-OBS-01 이후 로드맵

## Current SSOT

Latest baked line:

```txt
ash_pass3_SFT-GPU-OBS-01_telemetry_dashboard_baked.zip
```

OBS-01 has created a read-only telemetry dashboard/matrix drift console seal over:

```txt
RUN-01 strict GPU train
RUN-02 artifact intake
RUN-03 regression matrix
RUN-04 promotion bridge
RUN-05 operator approval
RUN-06 runtime attach dry-run
RUN-07 promotion apply candidate
RUN-08 current pointer switch
RUN-09 post-switch health
RUN-10 rollback drill
RUN-11 slot arbitration
RUN-12 lifecycle merge
RUN-13 operator action apply
SAFETY-01 GPU fault recovery
SAFETY-02 partial artifact quarantine
```

## Closed Contracts Preserved

```txt
No action controls.
No current pointer update.
No rollback execution.
No demotion apply.
No quarantine apply.
No registry mutation.
No lifecycle mutation.
No runtime SFT training.
No gradient write.
No optimizer step.
No textureSample weight fetch.
```

## Next Patch

# SFT-GPU-OBS-02 — Long-Horizon GPU Adapter Health Ledger / Runtime Drift Seal

## Purpose

OBS-02 should turn the single OBS-01 dashboard projection into a long-horizon append-only health ledger that can track adapter drift across repeated observations.

## OBS-02 Should Open

```txt
long-horizon GPU adapter health ledger
runtime drift trend event
health score trend
smoke pass/fail trend
fallback readiness drift
rollback availability drift
adapter digest drift
runtime backend drift
textureLoad guard drift
append-only observation event
```

## OBS-02 Must Keep Closed

```txt
current pointer update
operator action apply
rollback execution
demotion apply
quarantine apply
registry mutation
lifecycle mutation
runtime training
gradient write
optimizer step
silent correction
```

## Recommended Next Request

```txt
SFT-GPU-OBS-02 — Long-Horizon GPU Adapter Health Ledger / Runtime Drift Seal 명세
```
