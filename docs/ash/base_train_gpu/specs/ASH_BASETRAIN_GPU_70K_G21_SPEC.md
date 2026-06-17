# ASH-BASETRAIN-GPU-70K-G21 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G21
Controlled Sequence Append Execution Boundary /
Sequence Append Gate To Runtime Sequence Delta Candidate
No Decode No Loss No Backward
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G20` sequence append gate candidate and the `ASH-BASETRAIN-GPU-70K-G19` adopted token state descriptor to create a runtime sequence delta candidate.

G21 is a controlled sequence append execution-boundary patch, not a canonical sequence commit patch. It may create a runtime sequence delta candidate and append-operation candidate receipt, but it must not commit canonical sequence state, decode text, preview-decode token surfaces, create loss targets, compute loss, run backward, run optimizer, commit deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent adoption receipt: `ASH-BASETRAIN-GPU-70K-G19`
- Parent sequence append preflight: `ASH-BASETRAIN-GPU-70K-G20`
- Current patch: `ASH-BASETRAIN-GPU-70K-G21`
- Next patch: `ASH-BASETRAIN-GPU-70K-G22`
- New permission candidate: controlled sequence append boundary check and runtime sequence delta candidate creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g21_controlled_sequence_append_execution_boundary.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g21_controlled_sequence_append_execution_boundary.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G21_CONTROLLED_SEQUENCE_APPEND_EXECUTION_BOUNDARY.json`
- `specs/ASH_BASETRAIN_GPU_70K_G21_RUNTIME_SEQUENCE_DELTA_CANDIDATE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G21_SEQUENCE_APPEND_GATE_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G21_ADOPTED_TOKEN_TO_SEQUENCE_DELTA_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G21_NO_DECODE_LOSS_BACKWARD_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G21_SEQUENCE_DELTA_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G21_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G21_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G21_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G21_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- `*.md` markdown files
- full safetensors payloads
- training dataset payloads
- model checkpoints
- decoded text outputs
- canonical sequence commit outputs
- loss reports
- gradient dumps
- optimizer state dumps
- runtime benchmark reports

## Allowed in G21 runtime probe

- G20 sequence append preflight receipt read
- G20 sequence append gate candidate audit read
- G19 adopted token state audit read
- sequence append gate candidate acceptance check
- controlled sequence append boundary check
- runtime sequence delta candidate creation
- adopted token state to sequence delta lineage rebind
- no-decode/no-loss/no-backward boundary audit

## Forbidden in G21

- canonical sequence commit
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G21_CONTROLLED_SEQUENCE_APPEND_EXECUTION_BOUNDARY_READY_NO_LOCAL_SEQUENCE_DELTA_RUNTIME_CLAIM
```

The baked ZIP contains the G21 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G20 runtime PASS evidence were unavailable, so no local compile claim or runtime sequence delta candidate runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G21_CONTROLLED_SEQUENCE_APPEND_EXECUTION_BOUNDARY
```

G21 reaches runtime PASS only when the G20 sequence append gate candidate is accepted, the adopted token state is preserved, a runtime sequence delta candidate is created, and no canonical sequence commit, text decode, token surface preview decode, loss target creation, loss computation, backward, optimizer, delta commit, checkpoint mutation, weight mutation, or model-quality claim occurs.

## Next

```text
ASH-BASETRAIN-GPU-70K-G22
Runtime Sequence Delta Candidate Commit Gate /
Sequence Delta Candidate To Canonical Sequence Commit Preflight
No Decode No Loss No Backward
```
