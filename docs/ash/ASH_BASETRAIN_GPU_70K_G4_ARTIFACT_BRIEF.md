# ASH-BASETRAIN-GPU-70K-G4 Artifact Brief

```text
Patch: ASH-BASETRAIN-GPU-70K-G4
Title: Payload Source Contract Gate / Write-Ready Slot Map To Payload Source Availability Seal
Seal: No Payload Write / No GPU Upload / No Training
```

## Summary

`70K-G4` consumes the `70K-G3` lease plan and write-ready scaffold slot map, then checks whether a specified safetensors payload source candidate exists and whether its header/metadata can match the 201-slot scaffold map.

The baked ZIP excludes `docs/` and `.sha256` sidecars. This environment did not have Cargo/Rust available, so the ZIP is source-baked and structurally validated, but no local compile PASS is claimed.

## Generated Runtime Artifacts

```text
artifacts/ASH_BASETRAIN_GPU_70K_G4_PAYLOAD_SOURCE_CONTRACT_GATE.json
artifacts/ASH_BASETRAIN_GPU_70K_G4_PAYLOAD_SOURCE_AVAILABILITY_REPORT.json
artifacts/ASH_BASETRAIN_GPU_70K_G4_SLOT_TO_SOURCE_METADATA_MATCH_REPORT.json
artifacts/ASH_BASETRAIN_GPU_70K_G4_STATIC_CHECKS.json
artifacts/ASH_BASETRAIN_GPU_70K_G4_BAKE_MANIFEST.json
```

## Meaning of PASS

PASS means the payload source candidate exists, its safetensors header/metadata is readable, and its tensor key set, shape, dtype, and expected byte length match the G3 201-slot scaffold map.

PASS does not mean payload values are trusted, payload bytes were read, scaffold payload was written, GPU upload is ready, or training is ready.

## Next Gate

```text
ASH-BASETRAIN-GPU-70K-G5
Payload Source Slice Read Probe /
Available Payload Source To Selected Slot Bounded Read Evidence Seal
No Payload Write No GPU Upload No Training
```
