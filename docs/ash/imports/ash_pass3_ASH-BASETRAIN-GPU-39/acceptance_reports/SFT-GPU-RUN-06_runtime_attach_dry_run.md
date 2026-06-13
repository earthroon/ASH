# SFT-GPU-RUN-06 Acceptance

## Status

PASS_STATIC / PENDING_RUNTIME_ATTACH_DRY_RUN

## Scope

GPU-trained adapter runtime attach dry-run and current pointer guard seal.

## SSOT

- Source RUN-05 operator approval seal
- Promotion intent
- Artifact revalidation evidence
- Runtime compatibility evidence
- Adapter load sanity evidence
- Current pointer guard
- TextureLoad guard
- No runtime mutation guard
- Runtime attach dry-run seal

## Confirmed Static Gates

- RUN-05 operator approval seal is required.
- RUN-05 operator approval must be accepted.
- Promotion intent is required.
- Intent must approve runtime attach dry-run.
- Artifact revalidation is required.
- Manifest digest must match.
- Payload digest must match.
- Safetensors digest must match.
- Runtime model fingerprint is required.
- Target module compatibility is required.
- Adapter rank / alpha must match runtime expectation.
- Adapter shape compatibility is required.
- Adapter dtype compatibility is required.
- Adapter load sanity is required.
- TextureLoad guard must remain valid.
- textureSample / sampler / normalized UV weight fetch remain forbidden.
- Current pointer must remain unchanged.
- Promotion apply is forbidden.
- Runtime current pointer update is forbidden.
- Lifecycle mutation is forbidden.
- Slot action apply is forbidden.
- Rollback execution is forbidden.
- ASH current binding is forbidden.
- Runtime SFT training / gradient / optimizer are forbidden.

## Opened

- runtime attach dry-run
- adapter load sanity check
- target module compatibility check
- adapter artifact revalidation
- promotion intent consumption dry-run
- textureLoad guard revalidation
- current pointer unchanged guard

## Closed

- promotion apply
- runtime current pointer update
- current pointer switch
- slot ready mark
- lifecycle mutation
- slot action apply
- rollback execution
- ASH current binding
- runtime SFT training
- runtime gradient write
- runtime optimizer step

## Runtime Acceptance Pending

Requires actual runtime adapter loader dry-run from target backend.
