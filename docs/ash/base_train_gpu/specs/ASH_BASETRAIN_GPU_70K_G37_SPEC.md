# ASH-BASETRAIN-GPU-70K-G37 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G37
Non-Default Route Replay Smoke /
Non-Default Bind Receipt To Route Replay Receipt
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G36` non-default bind receipt and explicit runtime route candidate bind dryrun to create a non-default route replay smoke receipt and route replay receipt.

G37 is a non-default route replay smoke patch, not a runtime route bind execution, runtime default adoption, default route mutation, silent adoption, implicit route swap, production route switch, route promotion, operator approval, new final output, display surface write/rewrite/replacement, training, loss, backward, optimizer, model-delta, checkpoint, or weight mutation patch. It may accept the non-default bind receipt, accept the explicit runtime route candidate, create non-default route replay smoke, compare route replay digest, and create a route replay receipt as receipt-only. It must not execute runtime route bind, adopt a runtime default route, mutate the default route, perform silent adoption, perform implicit route swap, switch a production route, promote a route, auto-approve an operator, emit a new final output, write, rewrite, or replace the display surface, create loss targets, compute loss, run backward, run optimizer, materialize or commit model deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent runtime route candidate: `ASH-BASETRAIN-GPU-70K-G35`
- Parent non-default bind receipt: `ASH-BASETRAIN-GPU-70K-G36`
- Current patch: `ASH-BASETRAIN-GPU-70K-G37`
- Next patch: `ASH-BASETRAIN-GPU-70K-G38`
- New permission candidate: non-default route replay smoke and route replay receipt creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g37_non_default_route_replay_smoke.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g37_non_default_route_replay_smoke.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G37_NON_DEFAULT_ROUTE_REPLAY_SMOKE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G37_ROUTE_REPLAY_RECEIPT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G37_NON_DEFAULT_BIND_RECEIPT_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G37_ROUTE_REPLAY_DIGEST_COMPARE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G37_ROUTE_REPLAY_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G37_REPLAY_SMOKE_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G37_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G37_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G37_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G37_LOCAL_BAKE_VALIDATION.json`

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
- route promotion outputs
- loss reports
- gradient dumps
- optimizer state dumps
- model delta packets
- weight dumps
- runtime benchmark reports

## Allowed in G37 runtime probe

- G36 explicit runtime route candidate bind dryrun read
- G36 non-default bind receipt read
- G36 non-default route boundary audit read
- G35 explicit runtime route candidate read
- explicit runtime route candidate acceptance check
- non-default bind receipt acceptance check
- non-default route replay smoke creation
- route replay digest compare
- route replay receipt creation
- no-default-adoption/no-silent-adoption/no-loss/no-backward/no-optimizer boundary audit

## Forbidden in G37

- runtime route bind execution
- runtime default adoption
- default route mutation
- silent adoption
- implicit route swap
- production route switch
- route promotion
- operator approval auto-set
- operator approval mutation
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G37_NON_DEFAULT_ROUTE_REPLAY_SMOKE_READY_NO_LOCAL_ROUTE_REPLAY_STABILITY_RUNTIME_CLAIM
```

The baked ZIP contains the G37 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G36 runtime PASS evidence were unavailable, so no local compile claim or non-default route replay smoke runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G37_NON_DEFAULT_ROUTE_REPLAY_SMOKE
```

G37 reaches runtime PASS only when the G36 non-default bind receipt is accepted, the explicit runtime route candidate is accepted, a non-default route replay smoke is created, route replay digest is compared, and a route replay receipt is created as receipt-only without runtime route bind execution, runtime default adoption, default route mutation, silent adoption, implicit route swap, production route switch, route promotion, operator auto-approval, new final output emission, display surface write, display surface rewrite, display surface replacement, loss target creation, loss computation, backward, optimizer, model delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G38
Route Replay Receipt Stability Audit /
Route Replay Receipt To Non-Default Stability Ledger
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```
