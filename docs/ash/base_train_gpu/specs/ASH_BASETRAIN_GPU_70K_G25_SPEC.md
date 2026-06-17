# ASH-BASETRAIN-GPU-70K-G25 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G25
Controlled Token Decode Surface Candidate /
Decode Gate Candidate To Escaped Text Surface Draft
No Text Commit No Loss No Backward
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G24` committed sequence state decode preflight and decode gate candidate to create a controlled token decode surface candidate and escaped text surface draft envelope.

G25 is a decode surface draft patch, not a text commit or final output patch. It may create a controlled token decode surface candidate, create an escaped text surface draft envelope, and audit text surface escaping. It must not create text commits, emit final text, emit user-visible output, create loss targets, compute loss, run backward, run optimizer, materialize or commit model deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent sequence state seal: `ASH-BASETRAIN-GPU-70K-G23`
- Parent decode preflight: `ASH-BASETRAIN-GPU-70K-G24`
- Current patch: `ASH-BASETRAIN-GPU-70K-G25`
- Next patch: `ASH-BASETRAIN-GPU-70K-G26`
- New permission candidate: controlled token decode surface candidate and escaped text surface draft envelope creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g25_controlled_token_decode_surface_candidate.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g25_controlled_token_decode_surface_candidate.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G25_CONTROLLED_TOKEN_DECODE_SURFACE_CANDIDATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G25_ESCAPED_TEXT_SURFACE_DRAFT_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G25_DECODE_GATE_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G25_TEXT_SURFACE_ESCAPE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G25_NO_TEXT_COMMIT_LOSS_BACKWARD_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G25_DECODE_SURFACE_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G25_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G25_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G25_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G25_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- `*.md` markdown files
- full safetensors payloads
- training dataset payloads
- model checkpoints
- final text outputs
- text commit outputs
- loss reports
- gradient dumps
- optimizer state dumps
- model delta packets
- weight dumps
- runtime benchmark reports

## Allowed in G25 runtime probe

- G24 committed sequence state decode preflight read
- G24 decode gate candidate audit read
- G23 canonical sequence commit receipt read
- decode gate candidate acceptance check
- tokenizer binding readiness acceptance check
- controlled token decode surface candidate creation
- escaped text surface draft envelope creation
- text surface escape audit
- no-text-commit/no-loss/no-backward boundary audit

## Forbidden in G25

- text commit
- final text output
- user-visible output emit
- loss target creation
- loss computation
- loss backward
- backward execution
- gradient materialization
- optimizer state creation
- optimizer step
- model delta materialization
- model delta commit
- checkpoint mutation
- weight mutation
- runtime default adoption
- model quality claim
- training claim

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G25_CONTROLLED_TOKEN_DECODE_SURFACE_CANDIDATE_READY_NO_LOCAL_DECODE_SURFACE_RUNTIME_CLAIM
```

The baked ZIP contains the G25 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc`, concrete G24 runtime PASS evidence, and concrete tokenizer binding evidence were unavailable, so no local compile claim or controlled token decode surface candidate runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G25_CONTROLLED_TOKEN_DECODE_SURFACE_CANDIDATE
```

G25 reaches runtime PASS only when the G24 decode gate candidate is accepted, tokenizer binding readiness is accepted, a controlled token decode surface candidate is created, and an escaped text surface draft envelope is created without text commit, final text output, user-visible output emission, loss target creation, loss computation, backward, optimizer, model delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G26
Escaped Text Surface Review Gate /
Escaped Text Draft To Text Commit Preflight
No Final Emit No Loss No Backward
```
