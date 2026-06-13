# SFT-GPU-SAFETY-01 이후 로드맵

## Completed

SFT-GPU-SAFETY-01 sealed GPU train/runtime verification fault recovery for OOM, timeout, device lost, backend lost, kernel dispatch failure, textureLoad guard failure, and adapter write failure.

It explicitly keeps these paths closed after a GPU fault:

- CPU fallback as success
- failed/partial artifact registry intake
- failed/partial artifact promotion
- current pointer update
- runtime SFT training after fault
- gradient write after fault
- optimizer step after fault
- textureSample/sampler/normalized UV weight fetch
- silent backend switch
- silent registry correction

## Next Patch

SFT-GPU-SAFETY-02 — Partial Artifact Quarantine / Failed Train Output Guard

### Purpose

Take the quarantine_required verdict from SAFETY-01 and harden the artifact side:

- identify zero-byte safetensors
- identify partial manifest
- identify interrupted optimizer state
- identify failed parity payload
- prevent incomplete adapter payload from registry/promotion/current path
- optionally move failed outputs into a quarantine namespace/ledger without deleting evidence

### Still Closed Until Explicitly Opened

- production promotion of failed artifact
- silent cleanup that deletes evidence
- automatic candidate regeneration
- registry correction without operator review
