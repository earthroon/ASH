# ASH-BASETRAIN-GPU-70K-G40 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G40
Route Promotion Candidate Preflight /
Promotion Candidate To Explicit Promotion Dryrun Candidate
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G39` route promotion candidate, operator review gate, and operator review packet to create a route promotion candidate preflight and explicit promotion dryrun candidate.

G40 is a route promotion candidate preflight and explicit promotion dryrun candidate patch, not an operator approval, promotion dryrun execution, route promotion execution, runtime default adoption, default route mutation, silent adoption, implicit route swap, production route switch, runtime route bind execution, new final output, display surface write/rewrite/replacement, training, loss, backward, optimizer, model-delta, checkpoint, or weight mutation patch. It may accept the route promotion candidate, accept the operator review gate and packet, create route promotion candidate preflight, and create an explicit promotion dryrun candidate as candidate-only. It must not auto-approve the operator review, execute promotion dryrun, execute route promotion, adopt a runtime default route, mutate the default route, perform silent adoption, perform implicit route swap, switch a production route, emit a new final output, write, rewrite, or replace the display surface, create loss targets, compute loss, run backward, run optimizer, materialize or commit model deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent non-default stability ledger: `ASH-BASETRAIN-GPU-70K-G38`
- Parent route promotion candidate: `ASH-BASETRAIN-GPU-70K-G39`
- Current patch: `ASH-BASETRAIN-GPU-70K-G40`
- Next patch: `ASH-BASETRAIN-GPU-70K-G41`
- New permission candidate: route promotion candidate preflight and explicit promotion dryrun candidate creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g40_route_promotion_candidate_preflight.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g40_route_promotion_candidate_preflight.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G40_ROUTE_PROMOTION_CANDIDATE_PREFLIGHT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G40_EXPLICIT_PROMOTION_DRYRUN_CANDIDATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G40_ROUTE_PROMOTION_CANDIDATE_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G40_PROMOTION_PREFLIGHT_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G40_PROMOTION_DRYRUN_CANDIDATE_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G40_NO_DEFAULT_ADOPTION_SILENT_ADOPTION_LOSS_BACKWARD_OPTIMIZER_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G40_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G40_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G40_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G40_LOCAL_BAKE_VALIDATION.json`

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
- promotion dryrun execution outputs
- default route mutation outputs
- operator approval outputs
- loss reports
- gradient dumps
- optimizer state dumps
- model delta packets
- weight dumps
- runtime benchmark reports

## Allowed in G40 runtime probe

- G39 route promotion candidate read
- G39 operator review gate read
- G39 operator review packet read
- G39 route promotion candidate boundary audit read
- G38 non-default stability ledger read
- route promotion candidate acceptance check
- operator review gate acceptance check
- operator review packet acceptance check
- promotion candidate boundary acceptance check
- route promotion candidate preflight creation
- explicit promotion dryrun candidate creation
- no-default-adoption/no-silent-adoption/no-loss/no-backward/no-optimizer boundary audit

## Forbidden in G40

- promotion dryrun execution
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G40_ROUTE_PROMOTION_CANDIDATE_PREFLIGHT_READY_NO_LOCAL_PROMOTION_DRYRUN_RUNTIME_CLAIM
```

The baked ZIP contains the G40 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G39 runtime PASS evidence were unavailable, so no local compile claim or route promotion candidate preflight runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G40_ROUTE_PROMOTION_CANDIDATE_PREFLIGHT
```

G40 reaches runtime PASS only when the G39 route promotion candidate is accepted, the operator review gate is accepted, the operator review packet is accepted, the promotion candidate boundary is accepted, a route promotion candidate preflight is created, and an explicit promotion dryrun candidate is created as candidate-only without operator auto-approval, promotion dryrun execution, route promotion execution, runtime default adoption, default route mutation, silent adoption, implicit route swap, production route switch, new final output emission, display surface write, display surface rewrite, display surface replacement, loss target creation, loss computation, backward, optimizer, model delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G41
Explicit Promotion Dryrun Execution /
Promotion Dryrun Candidate To Dryrun Receipt
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```
