# ASH-BASETRAIN-GPU-70K-G41 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G41
Explicit Promotion Dryrun Execution /
Promotion Dryrun Candidate To Dryrun Receipt
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G40` explicit promotion dryrun candidate, route promotion candidate preflight, and dryrun candidate boundary audit to execute promotion dryrun and create a promotion dryrun receipt.

G41 is an explicit promotion dryrun execution and promotion dryrun receipt patch, not an operator approval, route promotion execution, runtime default adoption, default route mutation, silent adoption, implicit route swap, production route switch, runtime route bind execution, new final output, display surface write/rewrite/replacement, training, loss, backward, optimizer, model-delta, checkpoint, or weight mutation patch. It may accept the explicit promotion dryrun candidate, accept promotion preflight, accept the dryrun candidate boundary, execute promotion dryrun, compare promotion dryrun digest, and create a promotion dryrun receipt as receipt-only. It must not auto-approve the operator review, execute route promotion, adopt a runtime default route, mutate the default route, perform silent adoption, perform implicit route swap, switch a production route, emit a new final output, write, rewrite, or replace the display surface, create loss targets, compute loss, run backward, run optimizer, materialize or commit model deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent route promotion candidate: `ASH-BASETRAIN-GPU-70K-G39`
- Parent promotion dryrun candidate: `ASH-BASETRAIN-GPU-70K-G40`
- Current patch: `ASH-BASETRAIN-GPU-70K-G41`
- Next patch: `ASH-BASETRAIN-GPU-70K-G42`
- New permission candidate: explicit promotion dryrun execution and promotion dryrun receipt creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g41_explicit_promotion_dryrun_execution.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g41_explicit_promotion_dryrun_execution.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G41_EXPLICIT_PROMOTION_DRYRUN_EXECUTION.json`
- `specs/ASH_BASETRAIN_GPU_70K_G41_PROMOTION_DRYRUN_RECEIPT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G41_PROMOTION_DRYRUN_CANDIDATE_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G41_PROMOTION_DRYRUN_EXECUTION_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G41_PROMOTION_DRYRUN_RECEIPT_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G41_NO_DEFAULT_ADOPTION_SILENT_ADOPTION_LOSS_BACKWARD_OPTIMIZER_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G41_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G41_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G41_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G41_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- `*.md` markdown files
- full safetensors payloads
- training dataset payloads
- model checkpoints
- new final text outputs
- display surface write outputs
- display surface rewrite outputs
- display surface replacement outputs
- runtime default adoption outputs
- silent adoption outputs
- production route switch outputs
- route promotion execution outputs
- default route mutation outputs
- operator approval outputs
- loss reports
- gradient dumps
- optimizer state dumps
- model delta packets
- weight dumps
- runtime benchmark reports

## Allowed in G41 runtime probe

- G40 explicit promotion dryrun candidate read
- G40 route promotion candidate preflight read
- G40 promotion dryrun candidate boundary audit read
- G39 route promotion candidate read
- promotion dryrun candidate acceptance check
- promotion preflight acceptance check
- dryrun candidate boundary acceptance check
- explicit promotion dryrun execution
- promotion dryrun digest compare
- promotion dryrun receipt creation
- no-default-adoption/no-silent-adoption/no-loss/no-backward/no-optimizer boundary audit

## Forbidden in G41

- route promotion execution
- runtime default adoption
- default route mutation
- silent adoption
- implicit route swap
- production route switch
- operator approval auto-set
- operator approval mutation
- runtime route bind execution
- new final output emission
- display surface write
- display surface rewrite
- display surface replacement
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
- model quality claim
- training claim

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G41_EXPLICIT_PROMOTION_DRYRUN_EXECUTION_READY_NO_LOCAL_PROMOTION_RECEIPT_STABILITY_RUNTIME_CLAIM
```

The baked ZIP contains the G41 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G40 runtime PASS evidence were unavailable, so no local compile claim or explicit promotion dryrun execution runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G41_EXPLICIT_PROMOTION_DRYRUN_EXECUTION
```

G41 reaches runtime PASS only when the G40 explicit promotion dryrun candidate is accepted, the route promotion candidate preflight is accepted, the dryrun candidate boundary is accepted, promotion dryrun is executed, promotion dryrun digest is compared, and a promotion dryrun receipt is created as receipt-only without operator auto-approval, route promotion execution, runtime default adoption, default route mutation, silent adoption, implicit route swap, production route switch, new final output emission, display surface write, display surface rewrite, display surface replacement, loss target creation, loss computation, backward, optimizer, model delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G42
Promotion Dryrun Receipt Stability Audit /
Dryrun Receipt To Promotion Stability Ledger
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```
