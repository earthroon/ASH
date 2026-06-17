# ASH-BASETRAIN-GPU-70K-G26 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G26
Escaped Text Surface Review Gate /
Escaped Text Draft To Text Commit Preflight
No Final Emit No Loss No Backward
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G25` controlled token decode surface candidate and escaped text surface draft envelope to create an escaped text surface review gate, draft safety review receipt, and text commit preflight descriptor.

G26 is a text commit preflight patch, not a text commit or final output patch. It may accept the escaped text surface draft, accept the text surface escape audit, create a review gate, create a draft safety review receipt, and create a text commit preflight descriptor. It must not create text commits, emit final text, emit user-visible output, expose raw unescaped text, create loss targets, compute loss, run backward, run optimizer, materialize or commit model deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent decode surface draft: `ASH-BASETRAIN-GPU-70K-G25`
- Current patch: `ASH-BASETRAIN-GPU-70K-G26`
- Next patch: `ASH-BASETRAIN-GPU-70K-G27`
- New permission candidate: escaped text surface review gate and text commit preflight descriptor creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g26_escaped_text_surface_review_gate.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g26_escaped_text_surface_review_gate.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G26_ESCAPED_TEXT_SURFACE_REVIEW_GATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G26_TEXT_COMMIT_PREFLIGHT_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G26_ESCAPED_TEXT_DRAFT_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G26_DRAFT_SAFETY_REVIEW_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G26_NO_FINAL_EMIT_LOSS_BACKWARD_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G26_TEXT_COMMIT_PREFLIGHT_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G26_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G26_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G26_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G26_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- `*.md` markdown files
- full safetensors payloads
- training dataset payloads
- model checkpoints
- final text outputs
- user-visible text outputs
- text commit outputs
- raw unescaped text dumps
- loss reports
- gradient dumps
- optimizer state dumps
- model delta packets
- weight dumps
- runtime benchmark reports

## Allowed in G26 runtime probe

- G25 controlled token decode surface candidate read
- G25 escaped text surface draft audit read
- G25 text surface escape audit read
- escaped text surface draft acceptance check
- text surface escape audit acceptance check
- escaped text surface review gate creation
- draft safety review receipt creation
- text commit preflight descriptor creation
- no-final-emit/no-loss/no-backward boundary audit

## Forbidden in G26

- text commit
- final text emit
- user-visible output emit
- raw unescaped text exposure
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G26_ESCAPED_TEXT_SURFACE_REVIEW_GATE_READY_NO_LOCAL_TEXT_COMMIT_PREFLIGHT_RUNTIME_CLAIM
```

The baked ZIP contains the G26 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G25 runtime PASS evidence were unavailable, so no local compile claim or escaped text surface review gate runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G26_ESCAPED_TEXT_SURFACE_REVIEW_GATE
```

G26 reaches runtime PASS only when the G25 escaped text surface draft is accepted, the text surface escape audit is accepted, an escaped text surface review gate is created, a draft safety review receipt is created, and a text commit preflight descriptor is created without text commit, final text emit, user-visible output emission, raw unescaped text exposure, loss target creation, loss computation, backward, optimizer, model delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G27
Controlled Text Commit Receipt /
Text Commit Preflight To Committed Text Surface Seal
No Final Emit No Loss No Backward
```
