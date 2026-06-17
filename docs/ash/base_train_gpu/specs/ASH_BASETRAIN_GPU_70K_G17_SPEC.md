# ASH-BASETRAIN-GPU-70K-G17 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G17
Selected Token Draft Commit Preflight /
Selected Token Draft To Commit Gate Candidate
No Decode No Sequence Append No Loss
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G16` operator-reviewed selected token draft envelope to create a commit preflight receipt and commit gate candidate.

G17 is a commit preflight patch, not a token commit patch. It may range-check and lineage-check a selected token draft, then create a commit gate candidate. It must not commit a token, adopt a token into runtime state, decode text, append sequence state, compute loss, run backward, run optimizer, commit deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent candidate gate: `ASH-BASETRAIN-GPU-70K-G15`
- Parent selected token draft: `ASH-BASETRAIN-GPU-70K-G16`
- Current patch: `ASH-BASETRAIN-GPU-70K-G17`
- Next patch: `ASH-BASETRAIN-GPU-70K-G18`
- New permission candidate: selected token draft commit preflight and commit gate candidate creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g17_selected_token_draft_commit_preflight.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g17_selected_token_draft_commit_preflight.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G17_SELECTED_TOKEN_DRAFT_COMMIT_PREFLIGHT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G17_COMMIT_GATE_CANDIDATE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G17_SELECTED_TOKEN_DRAFT_RANGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G17_SELECTED_TOKEN_DRAFT_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G17_COMMIT_PREFLIGHT_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G17_NO_DECODE_SEQUENCE_APPEND_LOSS_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G17_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G17_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G17_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G17_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- `*.md` markdown files
- full safetensors payloads
- training dataset payloads
- model checkpoints
- delta packets
- token commit receipts
- token decode outputs
- sequence append outputs
- loss reports
- gradient dumps
- optimizer state dumps
- runtime benchmark reports

## Allowed in G17 runtime probe

- G16 selected token draft receipt read
- G16 selected token draft envelope audit read
- G15 candidate envelope audit read
- selected token draft range check
- selected token draft lineage rebind
- commit preflight policy check
- commit gate candidate descriptor creation
- no-decode/no-sequence-append/no-loss boundary audit

## Forbidden in G17

- token commit
- runtime token adoption
- text decode
- token surface preview decode
- sequence append
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G17_SELECTED_TOKEN_DRAFT_COMMIT_PREFLIGHT_READY_NO_LOCAL_COMMIT_PREFLIGHT_RUNTIME_CLAIM
```

The baked ZIP contains the G17 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G16 runtime PASS evidence were unavailable, so no local compile claim or selected token draft commit preflight runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G17_SELECTED_TOKEN_DRAFT_COMMIT_PREFLIGHT
```

G17 reaches runtime PASS only when the G16 selected token draft envelope is accepted, the selected token draft is range-checked and lineage-checked, and a commit gate candidate is created without token commit, runtime adoption, text decode, sequence append, loss computation, backward, optimizer, delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G18
Controlled Token Commit Boundary /
Commit Gate Candidate To Runtime Token Adoption Preflight
No Decode No Sequence Append No Loss
```
