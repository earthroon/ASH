# ASH-BASETRAIN-GPU-70K-G43 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G43
Promotion Stability Ledger Operator Review Gate /
Promotion Stability Ledger To Route Promotion Execution Candidate
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```

## Purpose

G43 consumes the `ASH-BASETRAIN-GPU-70K-G42` promotion stability ledger and creates two candidate-only outputs:

1. promotion stability ledger operator review gate
2. route promotion execution candidate

G43 creates review/candidate surfaces only. It does not approve the operator review and does not execute route promotion.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent route promotion candidate: `ASH-BASETRAIN-GPU-70K-G39`
- Parent promotion dryrun candidate: `ASH-BASETRAIN-GPU-70K-G40`
- Parent promotion dryrun receipt: `ASH-BASETRAIN-GPU-70K-G41`
- Parent promotion stability ledger: `ASH-BASETRAIN-GPU-70K-G42`
- Current patch: `ASH-BASETRAIN-GPU-70K-G43`
- Next patch: `ASH-BASETRAIN-GPU-70K-G44`

## Implementation style

G43 is baked in a lookup-table-first and match-based boundary style.

- `EXPECTED_STATE_LUT` holds the expected truth table.
- `G43ProbeKey` enumerates the boundary fields.
- `expected_value(...)` uses `match` for expected state lookup.
- `observed_value(...)` uses `match` for receipt field projection.
- `classify_boundary(...)` uses `match` to map observed mismatches to `G43FailureReason`.
- Forbidden callsite patterns are kept in static receipt JSON, not in source, to prevent source self-hit contamination.

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g43_promotion_stability_ledger_operator_review_gate.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g43_promotion_stability_ledger_operator_review_gate.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G43_PROMOTION_STABILITY_LEDGER_OPERATOR_REVIEW_GATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G43_ROUTE_PROMOTION_EXECUTION_CANDIDATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G43_PROMOTION_STABILITY_LEDGER_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G43_OPERATOR_REVIEW_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G43_ROUTE_PROMOTION_EXECUTION_CANDIDATE_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G43_NO_DEFAULT_ADOPTION_SILENT_ADOPTION_LOSS_BACKWARD_OPTIMIZER_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G43_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G43_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G43_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G43_LOCAL_BAKE_VALIDATION.json`

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

## Allowed in G43 runtime probe

- Read G42 promotion dryrun receipt stability audit
- Read G42 promotion stability ledger
- Read G42 promotion stability digest consistency audit
- Read G41 promotion dryrun receipt
- Check promotion stability ledger, dryrun stability audit, and digest consistency acceptance
- Create operator review gate
- Create operator review packet
- Create route promotion execution candidate
- Validate state through lookup-table and match-based boundary classification
- Audit no-default-adoption, no-silent-adoption, no-loss, no-backward, and no-optimizer boundary

## Closed in G43

G43 must keep closed: operator auto-approval, route promotion execution, runtime default adoption, default route mutation, silent adoption, implicit route swap, production route switch, runtime route bind execution, final output emission, display surface writes, loss, backward, optimizer, model delta, checkpoint mutation, and weight mutation.

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G43_PROMOTION_STABILITY_LEDGER_OPERATOR_REVIEW_GATE_READY_NO_LOCAL_ROUTE_PROMOTION_RUNTIME_CLAIM
```

The baked ZIP contains the G43 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G42 runtime PASS evidence were unavailable, so no local compile claim or promotion stability ledger operator review gate runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G43_PROMOTION_STABILITY_LEDGER_OPERATOR_REVIEW_GATE
```

G43 reaches runtime PASS only when the G42 promotion stability ledger, dryrun stability audit, and digest consistency evidence are accepted, an operator review gate is created, an operator review packet is created, and a route promotion execution candidate is created as candidate-only while every closed boundary remains closed.

## Next

```text
ASH-BASETRAIN-GPU-70K-G44
Route Promotion Execution Candidate Preflight /
Execution Candidate To Explicit Route Promotion Dryrun
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```
