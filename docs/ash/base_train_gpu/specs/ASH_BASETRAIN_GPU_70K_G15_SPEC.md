# ASH-BASETRAIN-GPU-70K-G15 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G15
Controlled Token Selection Candidate Gate /
TopK Preflight Descriptor To Operator Review
No Token Commit No Decode No Loss
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G14` descriptor-only top-k preflight and selection gate candidate to create a descriptor-only token selection candidate envelope and operator review queue item.

G15 is a candidate review-gate patch, not a token selection patch. It may create a token selection candidate envelope and queue an operator review item with `REVIEW_REQUIRED`, but it must not execute actual top-k, materialize top-k values or indices, run argmax, run sampling, select token IDs, commit tokens, decode text, append sequence state, compute loss, run backward, run optimizer, commit deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent semantic surface: `ASH-BASETRAIN-GPU-70K-G13`
- Parent top-k preflight: `ASH-BASETRAIN-GPU-70K-G14`
- Current patch: `ASH-BASETRAIN-GPU-70K-G15`
- Next patch: `ASH-BASETRAIN-GPU-70K-G16`
- New permission candidate: descriptor-only token selection candidate envelope and operator review queue item creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g15_controlled_token_selection_candidate_gate.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g15_controlled_token_selection_candidate_gate.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G15_CONTROLLED_TOKEN_SELECTION_CANDIDATE_GATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G15_TOKEN_SELECTION_CANDIDATE_ENVELOPE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G15_OPERATOR_REVIEW_QUEUE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G15_SELECTION_POLICY_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G15_TOPK_PREFLIGHT_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G15_NO_TOKEN_COMMIT_DECODE_LOSS_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G15_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G15_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G15_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G15_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- `*.md` markdown files
- full safetensors payloads
- training dataset payloads
- model checkpoints
- delta packets
- top-k result dumps
- token selection dumps
- token commit receipts
- token decode outputs
- sequence append outputs
- loss reports
- gradient dumps
- optimizer state dumps
- runtime benchmark reports

## Allowed in G15 runtime probe

- G14 top-k preflight receipt read
- G14 selection gate audit read
- G13 semantic surface gate receipt read
- top-k preflight descriptor acceptance check
- selection gate candidate descriptor acceptance check
- token selection candidate envelope draft creation
- operator review queue item creation
- no-token-commit/no-decode/no-loss boundary audit

## Forbidden in G15

- actual top-k execution
- top-k values materialization
- top-k indices materialization
- argmax execution
- sampling execution
- token ID selection
- token commit
- text decode
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G15_CONTROLLED_TOKEN_SELECTION_CANDIDATE_GATE_READY_NO_LOCAL_CANDIDATE_GATE_RUNTIME_CLAIM
```

The baked ZIP contains the G15 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G14 runtime PASS evidence were unavailable, so no local compile claim or controlled token selection candidate gate runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G15_CONTROLLED_TOKEN_SELECTION_CANDIDATE_GATE
```

G15 reaches runtime PASS only when the G14 descriptor-only top-k preflight and selection gate candidate are accepted, a descriptor-only token selection candidate envelope is created, and an operator review queue item is created with review required, without actual top-k execution, top-k value or index materialization, token ID selection, token commit, text decode, sequence append, loss computation, backward, optimizer, delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G16
Operator Reviewed Controlled Token ID Selection /
Candidate Envelope To Selected Token Draft
No Token Commit No Decode No Loss
```
