# ASH-BASETRAIN-GPU-70K-G44 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G44
Route Promotion Execution Candidate Preflight /
Execution Candidate To Explicit Route Promotion Dryrun
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```

## Purpose

G44 consumes the `ASH-BASETRAIN-GPU-70K-G43` route promotion execution candidate and creates two receipt-only outputs:

1. route promotion execution candidate preflight
2. explicit route promotion dryrun receipt

G44 executes the explicit route promotion dryrun only. It does not execute route promotion and does not adopt the default route.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent promotion stability ledger: `ASH-BASETRAIN-GPU-70K-G42`
- Parent route promotion execution candidate: `ASH-BASETRAIN-GPU-70K-G43`
- Current patch: `ASH-BASETRAIN-GPU-70K-G44`
- Next patch: `ASH-BASETRAIN-GPU-70K-G45`

## Implementation style

G44 is baked in a lookup-table-first and match-based boundary style.

- `EXPECTED_STATE_LUT` holds the expected truth table.
- `G44ProbeKey` enumerates the boundary fields.
- `expected_value(...)` uses `match` for expected state lookup.
- `observed_value(...)` uses `match` for receipt field projection.
- `classify_boundary(...)` uses `match` to map observed mismatches to `G44FailureReason`.
- Forbidden callsite patterns are kept in static receipt JSON, not in source, to prevent source self-hit contamination.

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g44_route_promotion_execution_candidate_preflight.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g44_route_promotion_execution_candidate_preflight.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G44_ROUTE_PROMOTION_EXECUTION_CANDIDATE_PREFLIGHT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G44_EXPLICIT_ROUTE_PROMOTION_DRYRUN_RECEIPT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G44_ROUTE_PROMOTION_EXECUTION_CANDIDATE_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G44_ROUTE_PROMOTION_DRYRUN_EXECUTION_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G44_ROUTE_PROMOTION_DRYRUN_RECEIPT_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G44_NO_DEFAULT_ADOPTION_SILENT_ADOPTION_LOSS_BACKWARD_OPTIMIZER_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G44_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G44_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G44_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G44_LOCAL_BAKE_VALIDATION.json`

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

## Allowed in G44 runtime probe

- Read G43 route promotion execution candidate
- Read G43 promotion stability ledger operator review gate
- Read G43 operator review packet
- Read G43 route promotion execution candidate boundary audit
- Read G42 promotion stability ledger
- Check execution candidate, review gate, review packet, and candidate boundary acceptance
- Create route promotion execution candidate preflight
- Execute explicit route promotion dryrun
- Compare route promotion dryrun digest
- Create explicit route promotion dryrun receipt
- Validate state through lookup-table and match-based boundary classification
- Audit no-default-adoption, no-silent-adoption, no-loss, no-backward, and no-optimizer boundary

## Closed in G44

G44 must keep closed: route promotion execution, runtime default adoption, default route mutation, silent adoption, implicit route swap, production route switch, operator auto-approval, runtime route bind execution, final output emission, display surface writes, loss, backward, optimizer, model delta, checkpoint mutation, and weight mutation.

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G44_ROUTE_PROMOTION_EXECUTION_CANDIDATE_PREFLIGHT_READY_NO_LOCAL_ROUTE_PROMOTION_RUNTIME_CLAIM
```

The baked ZIP contains the G44 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G43 runtime PASS evidence were unavailable, so no local compile claim or route promotion execution candidate preflight runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G44_ROUTE_PROMOTION_EXECUTION_CANDIDATE_PREFLIGHT
```

G44 reaches runtime PASS only when the G43 route promotion execution candidate, review gate, review packet, and execution candidate boundary are accepted, a preflight is created, explicit route promotion dryrun is executed, a digest is compared, and a receipt is created as receipt-only while every closed boundary remains closed.

## Next

```text
ASH-BASETRAIN-GPU-70K-G45
Route Promotion Dryrun Receipt Stability Audit /
Dryrun Receipt To Route Promotion Stability Ledger
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```
