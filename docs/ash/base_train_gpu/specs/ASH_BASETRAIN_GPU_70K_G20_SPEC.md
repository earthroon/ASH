# ASH-BASETRAIN-GPU-70K-G20 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G20
Adopted Token State Sequence Append Preflight /
Adopted Token State To Sequence Append Gate
No Decode No Loss No Backward
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G19` runtime token adoption receipt and adopted token state descriptor to create a sequence append preflight descriptor and sequence append gate candidate.

G20 is a sequence append preflight patch, not a sequence append execution patch. It may create a sequence append preflight descriptor and append gate candidate, but it must not append to sequence state, mutate runtime sequence state, decode text, preview-decode token surfaces, create loss targets, compute loss, run backward, run optimizer, commit deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent commit boundary: `ASH-BASETRAIN-GPU-70K-G18`
- Parent adopted token state: `ASH-BASETRAIN-GPU-70K-G19`
- Current patch: `ASH-BASETRAIN-GPU-70K-G20`
- Next patch: `ASH-BASETRAIN-GPU-70K-G21`
- New permission candidate: adopted token state sequence append preflight and sequence append gate candidate creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g20_adopted_token_state_sequence_append_preflight.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g20_adopted_token_state_sequence_append_preflight.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G20_ADOPTED_TOKEN_STATE_SEQUENCE_APPEND_PREFLIGHT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G20_SEQUENCE_APPEND_GATE_CANDIDATE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G20_ADOPTED_TOKEN_STATE_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G20_SEQUENCE_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G20_NO_DECODE_LOSS_BACKWARD_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G20_SEQUENCE_APPEND_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G20_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G20_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G20_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G20_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- `*.md` markdown files
- full safetensors payloads
- training dataset payloads
- model checkpoints
- delta packets
- decoded text outputs
- sequence append outputs
- runtime sequence dumps
- loss reports
- gradient dumps
- optimizer state dumps
- runtime benchmark reports

## Allowed in G20 runtime probe

- G19 runtime token adoption receipt read
- G19 adopted token state audit read
- G18 runtime token adoption preflight lineage read
- G17 commit gate lineage read
- adopted token state acceptance check
- sequence append preflight descriptor creation
- sequence append gate candidate descriptor creation
- no-decode/no-loss/no-backward boundary audit

## Forbidden in G20

- actual sequence append
- runtime sequence mutation
- text decode
- token surface preview decode
- loss target creation
- loss computation
- loss backward
- backward execution
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G20_ADOPTED_TOKEN_STATE_SEQUENCE_APPEND_PREFLIGHT_READY_NO_LOCAL_SEQUENCE_APPEND_PREFLIGHT_RUNTIME_CLAIM
```

The baked ZIP contains the G20 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G19 runtime PASS evidence were unavailable, so no local compile claim or adopted token state sequence append preflight runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G20_ADOPTED_TOKEN_STATE_SEQUENCE_APPEND_PREFLIGHT
```

G20 reaches runtime PASS only when the G19 adopted token state descriptor is accepted, a sequence append preflight descriptor and sequence append gate candidate are created, and no actual sequence append, runtime sequence mutation, text decode, token surface preview decode, loss target creation, loss computation, backward, optimizer, delta commit, checkpoint mutation, weight mutation, or model-quality claim occurs.

## Next

```text
ASH-BASETRAIN-GPU-70K-G21
Controlled Sequence Append Execution Boundary /
Sequence Append Gate To Runtime Sequence Delta Candidate
No Decode No Loss No Backward
```
