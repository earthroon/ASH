# ASH-BASETRAIN-GPU-70K-G46 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G46
Route Promotion Stability Ledger Operator Review Gate /
Route Promotion Stability Ledger To Explicit Promotion Execution Gate
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```

## Purpose

G46 consumes the `ASH-BASETRAIN-GPU-70K-G45` route promotion stability ledger and creates two gate-only outputs:

1. route promotion stability ledger operator review gate
2. explicit promotion execution gate

G46 creates review/gate surfaces only. It does not approve the operator review and does not execute route promotion.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent route promotion execution candidate: `ASH-BASETRAIN-GPU-70K-G43`
- Parent route promotion dryrun receipt: `ASH-BASETRAIN-GPU-70K-G44`
- Parent route promotion stability ledger: `ASH-BASETRAIN-GPU-70K-G45`
- Current patch: `ASH-BASETRAIN-GPU-70K-G46`
- Next patch: `ASH-BASETRAIN-GPU-70K-G47`

## Implementation style

G46 is baked in a lookup-table-first and match-based boundary style.

- `EXPECTED_STATE_LUT` holds the expected truth table.
- `G46ProbeKey` enumerates the boundary fields.
- `expected_value(...)` uses `match` for expected state lookup.
- `observed_value(...)` uses `match` for receipt field projection.
- `classify_boundary(...)` uses `match` to map observed mismatches to `G46FailureReason`.
- Forbidden callsite patterns are kept in static receipt JSON, not in source, to prevent source self-hit contamination.

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g46_route_promotion_stability_ledger_operator_review_gate.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g46_route_promotion_stability_ledger_operator_review_gate.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G46_ROUTE_PROMOTION_STABILITY_LEDGER_OPERATOR_REVIEW_GATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G46_EXPLICIT_PROMOTION_EXECUTION_GATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G46_ROUTE_PROMOTION_STABILITY_LEDGER_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G46_OPERATOR_REVIEW_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G46_EXPLICIT_PROMOTION_EXECUTION_GATE_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G46_NO_DEFAULT_ADOPTION_SILENT_ADOPTION_LOSS_BACKWARD_OPTIMIZER_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G46_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G46_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G46_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G46_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- `*.md` markdown files
- full safetensors payloads
- training dataset payloads
- model checkpoints
- final output artifacts
- display surface artifacts
- route/default adoption artifacts
- promotion execution artifacts
- approval artifacts
- loss/backward/optimizer artifacts
- model delta/checkpoint/weight artifacts

## Allowed in G46 runtime probe

- Read G45 route promotion dryrun receipt stability audit
- Read G45 route promotion stability ledger
- Read G45 route promotion stability digest consistency audit
- Read G44 explicit route promotion dryrun receipt
- Check route promotion stability ledger, dryrun stability audit, and digest consistency acceptance
- Create operator review gate
- Create operator review packet
- Create explicit promotion execution gate
- Validate state through lookup-table and match-based boundary classification
- Audit no-default-adoption, no-silent-adoption, no-loss, no-backward, and no-optimizer boundary

## Closed in G46

G46 must keep closed: operator auto-approval, route promotion execution, runtime default adoption, default route mutation, silent adoption, implicit route swap, production route switch, runtime route bind execution, final output emission, display surface writes, loss, backward, optimizer, model delta, checkpoint mutation, and weight mutation.

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G46_ROUTE_PROMOTION_STABILITY_LEDGER_OPERATOR_REVIEW_GATE_READY_NO_LOCAL_ROUTE_PROMOTION_RUNTIME_CLAIM
```

The baked ZIP contains the G46 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G45 runtime PASS evidence were unavailable, so no local compile claim or route promotion stability ledger operator review gate runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G46_ROUTE_PROMOTION_STABILITY_LEDGER_OPERATOR_REVIEW_GATE
```

G46 reaches runtime PASS only when the G45 route promotion stability ledger, dryrun stability audit, and digest consistency evidence are accepted, an operator review gate is created, an operator review packet is created, and an explicit promotion execution gate is created as gate-only while every closed boundary remains closed.

## Next

```text
ASH-BASETRAIN-GPU-70K-G47
Explicit Promotion Execution Gate Preflight /
Execution Gate To Controlled Promotion Execution Candidate
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```
