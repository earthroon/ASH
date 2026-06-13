# SFT-GPU-SAFETY-02 이후 로드맵

## Current SSOT

Latest baked line:

```txt
SFT-GPU-SAFETY-02 — Partial Artifact Quarantine / Failed Train Output Guard
```

The line now has:

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
RUN-12 lifecycle ledger merge
RUN-13 operator-reviewed action apply
SAFETY-01 GPU fault recovery
SAFETY-02 partial artifact quarantine
```

## What SAFETY-02 Closed

```txt
failed train output registry intake
failed train output promotion
failed train output current pointer binding
failed train output lifecycle action path
auto manifest repair
silent digest replacement
silent registry correction
CPU fallback success artifact acceptance
textureSample weight fetch
```

## Recommended Next Patch

```txt
SFT-GPU-OBS-01 — Strict GPU Train Telemetry Dashboard / Matrix Drift Console Seal
```

## OBS-01 Purpose

Create a long-lived telemetry view for strict GPU train, promotion, post-switch health, rollback drill, slot arbitration, lifecycle merge, operator action apply, fault recovery, and partial artifact quarantine.

## OBS-01 Should Read

```txt
loss direction
adapter delta norm
GPU backend fingerprint
CPU fallback attempted/accepted split
save-reload parity
current adapter health score
fallback readiness
rollback availability
post-switch smoke failure rate
operator action apply outcomes
fault kind/stage
quarantine namespace count
partial artifact kind histogram
```

## OBS-01 Must Not Do

```txt
no registry mutation
no promotion
no current pointer switch
no demotion/quarantine apply
no artifact auto repair
no digest replacement
no lifecycle action apply
```
