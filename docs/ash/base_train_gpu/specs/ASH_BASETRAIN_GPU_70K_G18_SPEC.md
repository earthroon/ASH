# ASH-BASETRAIN-GPU-70K-G18 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G18
Controlled Token Commit Boundary /
Commit Gate Candidate To Runtime Token Adoption Preflight
No Decode No Sequence Append No Loss
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G17` commit gate candidate and selected token draft lineage to create a controlled token commit boundary check and runtime token adoption preflight descriptor.

G18 is an adoption preflight patch, not a decode or sequence append patch. It may check the controlled token commit boundary and create a runtime token adoption preflight descriptor. It must not decode text, preview-decode token surfaces, append sequence state, mutate runtime sequence state, compute loss, run backward, run optimizer, commit deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent selected token draft: `ASH-BASETRAIN-GPU-70K-G16`
- Parent commit preflight: `ASH-BASETRAIN-GPU-70K-G17`
- Current patch: `ASH-BASETRAIN-GPU-70K-G18`
- Next patch: `ASH-BASETRAIN-GPU-70K-G19`
- New permission candidate: controlled token commit boundary check and runtime adoption preflight descriptor creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g18_controlled_token_commit_boundary.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g18_controlled_token_commit_boundary.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G18_CONTROLLED_TOKEN_COMMIT_BOUNDARY.json`
- `specs/ASH_BASETRAIN_GPU_70K_G18_RUNTIME_TOKEN_ADOPTION_PREFLIGHT_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G18_COMMIT_GATE_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G18_SELECTED_TOKEN_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G18_NO_DECODE_SEQUENCE_APPEND_LOSS_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G18_COMMIT_BOUNDARY_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G18_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G18_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G18_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G18_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- `*.md` markdown files
- full safetensors payloads
- training dataset payloads
- model checkpoints
- delta packets
- token decode outputs
- sequence append outputs
- loss reports
- gradient dumps
- optimizer state dumps
- runtime benchmark reports

## Allowed in G18 runtime probe

- G17 commit preflight receipt read
- G17 commit gate candidate audit read
- G16 selected token draft receipt read
- commit gate candidate acceptance check
- controlled token commit boundary check
- runtime token adoption preflight descriptor creation
- selected token draft lineage rebind
- no-decode/no-sequence-append/no-loss boundary audit

## Forbidden in G18

- text decode
- token surface preview decode
- sequence append
- runtime sequence mutation
- loss computation
- loss backward
- gradient materialization
- optimizer state creation
- optimizer step
- delta materialization
- delta commit
- checkpoint mutation
- weight mutation
- runtime default adoption
- model quality claim
- training claim

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G18_CONTROLLED_TOKEN_COMMIT_BOUNDARY_READY_NO_LOCAL_ADOPTION_PREFLIGHT_RUNTIME_CLAIM
```

The baked ZIP contains the G18 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G17 runtime PASS evidence were unavailable, so no local compile claim or runtime token adoption preflight runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G18_CONTROLLED_TOKEN_COMMIT_BOUNDARY
```

G18 reaches runtime PASS only when the G17 commit gate candidate is accepted, the controlled token commit boundary is checked, and a runtime token adoption preflight descriptor is created without text decode, token surface preview decode, sequence append, runtime sequence mutation, loss computation, backward, optimizer, delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G19
Runtime Token Adoption Receipt /
Commit Boundary To Adopted Token State
No Decode No Sequence Append No Loss
```
