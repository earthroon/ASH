# ASH-BASETRAIN-GPU-70K-G24 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G24
Committed Sequence State Decode Preflight /
Sequence State Seal To Decode Gate Candidate
No Text Output No Loss No Backward
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G23` canonical sequence commit receipt and canonical sequence state seal to create a committed sequence state decode preflight descriptor and decode gate candidate.

G24 is a decode preflight patch, not an actual text output patch. It may check committed sequence state integrity, check tokenizer binding readiness, create a decode preflight descriptor, and create a decode gate candidate. It must not create actual text output, create decoded strings, preview-decode token surfaces, create loss targets, compute loss, run backward, run optimizer, materialize or commit model deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent sequence commit preflight: `ASH-BASETRAIN-GPU-70K-G22`
- Parent sequence state seal: `ASH-BASETRAIN-GPU-70K-G23`
- Current patch: `ASH-BASETRAIN-GPU-70K-G24`
- Next patch: `ASH-BASETRAIN-GPU-70K-G25`
- New permission candidate: committed sequence state decode preflight and decode gate candidate creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g24_committed_sequence_state_decode_preflight.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g24_committed_sequence_state_decode_preflight.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G24_COMMITTED_SEQUENCE_STATE_DECODE_PREFLIGHT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G24_DECODE_GATE_CANDIDATE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G24_SEQUENCE_STATE_SEAL_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G24_TOKENIZER_BINDING_READINESS_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G24_NO_TEXT_OUTPUT_LOSS_BACKWARD_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G24_DECODE_PREFLIGHT_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G24_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G24_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G24_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G24_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- `*.md` markdown files
- full safetensors payloads
- training dataset payloads
- model checkpoints
- decoded text outputs
- text surface outputs
- loss reports
- gradient dumps
- optimizer state dumps
- model delta packets
- weight dumps
- runtime benchmark reports

## Allowed in G24 runtime probe

- G23 canonical sequence commit receipt read
- G23 canonical sequence state seal audit read
- G22 sequence commit gate lineage read
- committed sequence state integrity check
- tokenizer binding readiness check
- decode preflight descriptor creation
- decode gate candidate creation
- no-text-output/no-loss/no-backward boundary audit

## Forbidden in G24

- actual text output
- decoded string creation
- token surface preview decode
- token id to string emission
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G24_COMMITTED_SEQUENCE_STATE_DECODE_PREFLIGHT_READY_NO_LOCAL_DECODE_PREFLIGHT_RUNTIME_CLAIM
```

The baked ZIP contains the G24 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc`, concrete G23 runtime PASS evidence, and concrete tokenizer binding evidence were unavailable, so no local compile claim or committed sequence state decode preflight runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G24_COMMITTED_SEQUENCE_STATE_DECODE_PREFLIGHT
```

G24 reaches runtime PASS only when the G23 canonical sequence state seal is accepted, committed sequence state integrity is checked, tokenizer binding readiness is checked, a decode preflight descriptor and decode gate candidate are created, and no actual text output, decoded string creation, token surface preview decode, loss target creation, loss computation, backward, optimizer, model delta commit, checkpoint mutation, weight mutation, or model-quality claim occurs.

## Next

```text
ASH-BASETRAIN-GPU-70K-G25
Controlled Token Decode Surface Candidate /
Decode Gate Candidate To Escaped Text Surface Draft
No Text Commit No Loss No Backward
```
