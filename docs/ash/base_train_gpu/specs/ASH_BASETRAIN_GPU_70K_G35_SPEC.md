# ASH-BASETRAIN-GPU-70K-G35 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G35
Replay Adoption Candidate Runtime Bind Preflight /
Adoption Candidate To Explicit Runtime Route Candidate
No Silent Adoption No Loss No Backward No Optimizer
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G34` replay adoption candidate, operator review gate, operator review packet, and adoption boundary audit to create a runtime bind preflight and explicit runtime route candidate.

G35 is a runtime bind preflight and explicit route candidate patch, not an operator approval, runtime route bind execution, runtime default adoption, silent adoption, display surface write/rewrite/replacement, new final output, training, loss, backward, optimizer, model-delta, checkpoint, or weight mutation patch. It may accept the replay adoption candidate, accept the operator review gate and packet, create runtime bind preflight, and create an explicit runtime route candidate as candidate-only. It must not auto-approve the operator review, execute runtime route bind, adopt a runtime default route, perform silent adoption, perform implicit route swap, emit a new final output, write, rewrite, or replace the display surface, create loss targets, compute loss, run backward, run optimizer, materialize or commit model deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent replay adoption candidate: `ASH-BASETRAIN-GPU-70K-G34`
- Current patch: `ASH-BASETRAIN-GPU-70K-G35`
- Next patch: `ASH-BASETRAIN-GPU-70K-G36`
- New permission candidate: runtime bind preflight and explicit runtime route candidate creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g35_replay_adoption_candidate_runtime_bind_preflight.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g35_replay_adoption_candidate_runtime_bind_preflight.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G35_REPLAY_ADOPTION_CANDIDATE_RUNTIME_BIND_PREFLIGHT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G35_EXPLICIT_RUNTIME_ROUTE_CANDIDATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G35_REPLAY_ADOPTION_CANDIDATE_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G35_RUNTIME_BIND_PREFLIGHT_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G35_RUNTIME_ROUTE_CANDIDATE_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G35_NO_SILENT_ADOPTION_LOSS_BACKWARD_OPTIMIZER_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G35_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G35_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G35_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G35_LOCAL_BAKE_VALIDATION.json`

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
- runtime adoption outputs
- runtime route bind outputs
- default route mutation outputs
- loss reports
- gradient dumps
- optimizer state dumps
- model delta packets
- weight dumps
- runtime benchmark reports

## Allowed in G35 runtime probe

- G34 replay adoption candidate read
- G34 operator review gate read
- G34 operator review packet read
- G34 replay adoption boundary audit read
- G33 replay stability closure read
- replay adoption candidate acceptance check
- operator review gate acceptance check
- runtime bind preflight creation
- explicit runtime route candidate creation
- no-silent-adoption/no-loss/no-backward/no-optimizer boundary audit

## Forbidden in G35

- operator approval auto-set
- operator approval mutation
- replay adoption execution
- runtime route bind execution
- runtime default adoption
- silent adoption
- implicit route swap
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
- runtime default adoption
- model quality claim
- training claim

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G35_REPLAY_ADOPTION_CANDIDATE_RUNTIME_BIND_PREFLIGHT_READY_NO_LOCAL_RUNTIME_ROUTE_BIND_CLAIM
```

The baked ZIP contains the G35 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G34 runtime PASS evidence were unavailable, so no local compile claim or replay adoption candidate runtime bind preflight runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G35_REPLAY_ADOPTION_CANDIDATE_RUNTIME_BIND_PREFLIGHT
```

G35 reaches runtime PASS only when the G34 replay adoption candidate is accepted, the operator review gate is accepted, the operator review packet is accepted, runtime bind preflight is created, and an explicit runtime route candidate is created as candidate-only without operator auto-approval, runtime route bind execution, runtime default adoption, silent adoption, implicit route swap, new final output emission, display surface write, display surface rewrite, display surface replacement, loss target creation, loss computation, backward, optimizer, model delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G36
Explicit Runtime Route Candidate Bind Dryrun /
Runtime Route Candidate To Non-Default Bind Receipt
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```
