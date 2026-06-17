# ASH-BASETRAIN-GPU-70K-G4-R2 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G4-R2
Current Head SSOT Freeze /
G4-R1 Payload Source Contract State To Next Patch Anchor Seal
No Runtime Expansion No Training Claim
```

## Purpose

Freeze `ASH-BASETRAIN-GPU-70K-G4-R1` as the current BaseTrain 70K head SSOT anchor and emit the next allowed patch matrix for `ASH-BASETRAIN-GPU-70K-G5`.

## SSOT

- Domain: `subtitle_translation_assist`
- Current head: `ASH-BASETRAIN-GPU-70K-G4-R1`
- Freeze patch: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Next allowed patch: `ASH-BASETRAIN-GPU-70K-G5`
- Next permission candidate: bounded selected-slice payload read

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g4_r2_current_head_ssot_freeze.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g4_r2_current_head_ssot_freeze.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G4_R2_CURRENT_HEAD_SSOT_FREEZE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G4_R2_NEXT_ALLOWED_PATCH_MATRIX.json`
- `specs/ASH_BASETRAIN_GPU_70K_G4_R2_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G4_R2_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G4_R2_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G4_R2_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- full tensor payloads
- runtime training reports

## Forbidden in G4-R2

- payload byte read
- full tensor load
- tensor decode
- GPU upload
- bind group creation
- shader dispatch
- forward
- backward
- optimizer
- delta materialization
- checkpoint mutation
- runtime default adoption
- model quality claim
- training claim

## Acceptance

```text
PASS_ASH_BASETRAIN_GPU_70K_G4_R2_CURRENT_HEAD_SSOT_FREEZE
```

## Notes

This patch is a metadata-only freeze gate. It does not prove selected-slice read, GPU upload, forward execution, backward execution, optimizer execution, or model quality improvement. Those remain deferred to later patches, beginning with `ASH-BASETRAIN-GPU-70K-G5`.
