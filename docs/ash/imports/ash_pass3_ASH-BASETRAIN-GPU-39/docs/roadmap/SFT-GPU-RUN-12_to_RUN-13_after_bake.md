# SFT-GPU-RUN-12 이후 로드맵

## Current SSOT

`SFT-GPU-RUN-12` records the GPU-trained adapter lineage into an append-only lifecycle ledger event. It consumes RUN-11 slot arbitration output and does not apply any recommendation.

## What RUN-12 Opens

- training lineage event
- strict GPU train lineage entry
- artifact intake lineage entry
- regression matrix lineage entry
- promotion review lineage entry
- operator approval lineage entry
- runtime attach dry-run lineage entry
- promotion apply candidate lineage entry
- current pointer switch lineage entry
- post-switch health lineage entry
- rollback drill lineage entry
- slot arbitration lineage entry
- append-only lifecycle event
- lifecycle merge seal

## What RUN-12 Keeps Closed

- unreviewed action apply
- recommendation apply
- current pointer update
- rollback execution
- fallback activation
- actual demotion apply
- actual quarantine apply
- ASH current binding
- runtime SFT training
- runtime gradient write
- runtime optimizer step
- textureSample / sampler / normalized UV weight fetch
- silent CPU fallback success
- silent registry correction

## Next Patch

# SFT-GPU-RUN-13 — GPU-Trained Operator Action Apply / Lifecycle Transition Seal

RUN-13 is the first patch in this line that may apply an operator-reviewed lifecycle action. It must consume:

- RUN-11 slot arbitration recommendation
- RUN-12 lifecycle merge seal
- explicit operator review receipt

RUN-13 must still reject:

- unreviewed action apply
- recommendation mismatch apply
- silent registry correction
- runtime SFT training
- runtime gradient write
- runtime optimizer step

## Recommended Request

```txt
SFT-GPU-RUN-13 — GPU-Trained Operator Action Apply / Lifecycle Transition Seal 명세
```
