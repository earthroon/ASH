# ASH-BASETRAIN-GPU-70K-G30 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G30
Display Surface Regression Audit /
Display Surface Seal To Output Stability Ledger
No Loss No Backward No Optimizer
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G29` final output emission receipt and display surface seal to create a display surface regression audit and output stability ledger.

G30 is a display surface regression audit patch, not a new final output, surface rewrite, training, loss, backward, optimizer, model-delta, checkpoint, or weight mutation patch. It may accept the final output emission receipt, accept the display surface seal, check display surface digest replay, create a display surface regression audit, and create an output stability ledger. It must not emit a new final output, rewrite or mutate the display surface, create loss targets, compute loss, run backward, run optimizer, materialize or commit model deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent display surface seal: `ASH-BASETRAIN-GPU-70K-G29`
- Current patch: `ASH-BASETRAIN-GPU-70K-G30`
- Next patch: `ASH-BASETRAIN-GPU-70K-G31`
- New permission candidate: display surface regression audit and output stability ledger creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g30_display_surface_regression_audit.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g30_display_surface_regression_audit.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G30_DISPLAY_SURFACE_REGRESSION_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G30_OUTPUT_STABILITY_LEDGER.json`
- `specs/ASH_BASETRAIN_GPU_70K_G30_DISPLAY_SURFACE_SEAL_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G30_DISPLAY_SURFACE_DIGEST_REPLAY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G30_NO_LOSS_BACKWARD_OPTIMIZER_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G30_REGRESSION_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G30_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G30_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G30_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G30_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- `*.md` markdown files
- full safetensors payloads
- training dataset payloads
- model checkpoints
- new final text outputs
- display surface rewrite outputs
- loss reports
- gradient dumps
- optimizer state dumps
- model delta packets
- weight dumps
- runtime benchmark reports

## Allowed in G30 runtime probe

- G29 final output emission receipt read
- G29 display surface seal audit read
- G28 final output gate candidate audit read
- final output emission receipt acceptance check
- display surface seal acceptance check
- display surface digest replay check
- display surface regression audit creation
- output stability ledger creation
- no-loss/no-backward/no-optimizer boundary audit

## Forbidden in G30

- new final output emission
- display surface rewrite
- display surface mutation
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G30_DISPLAY_SURFACE_REGRESSION_AUDIT_READY_NO_LOCAL_OUTPUT_STABILITY_LEDGER_RUNTIME_CLAIM
```

The baked ZIP contains the G30 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G29 runtime PASS evidence were unavailable, so no local compile claim or display surface regression audit runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G30_DISPLAY_SURFACE_REGRESSION_AUDIT
```

G30 reaches runtime PASS only when the G29 final output emission receipt is accepted, the G29 display surface seal is accepted, display surface digest replay is checked, a display surface regression audit is created, and an output stability ledger is created without new final output emission, display surface rewrite, loss target creation, loss computation, backward, optimizer, model delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G31
Output Stability Ledger Replay Gate /
Stability Ledger To Deterministic Display Replay Candidate
No Loss No Backward No Optimizer
```
