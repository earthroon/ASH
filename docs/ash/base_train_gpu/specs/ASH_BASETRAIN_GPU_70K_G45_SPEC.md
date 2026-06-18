# ASH-BASETRAIN-GPU-70K-G45 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G45
Route Promotion Dryrun Receipt Stability Audit /
Dryrun Receipt To Route Promotion Stability Ledger
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```

## Purpose

G45 consumes the `ASH-BASETRAIN-GPU-70K-G44` explicit route promotion dryrun receipt and creates two ledger-only outputs:

1. route promotion dryrun receipt stability audit
2. route promotion stability ledger

G45 audits and ledgers the already-created dryrun receipt. It does not rerun the route promotion dryrun and does not execute route promotion.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent promotion stability ledger: `ASH-BASETRAIN-GPU-70K-G42`
- Parent route promotion execution candidate: `ASH-BASETRAIN-GPU-70K-G43`
- Parent route promotion dryrun receipt: `ASH-BASETRAIN-GPU-70K-G44`
- Current patch: `ASH-BASETRAIN-GPU-70K-G45`
- Next patch: `ASH-BASETRAIN-GPU-70K-G46`

## Implementation style

G45 is baked in a lookup-table-first and match-based boundary style.

- `EXPECTED_STATE_LUT` holds the expected truth table.
- `G45ProbeKey` enumerates the boundary fields.
- `expected_value(...)` uses `match` for expected state lookup.
- `observed_value(...)` uses `match` for receipt field projection.
- `classify_boundary(...)` uses `match` to map observed mismatches to `G45FailureReason`.
- Forbidden callsite patterns are kept in static receipt JSON, not in source, to prevent source self-hit contamination.

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g45_route_promotion_dryrun_receipt_stability_audit.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g45_route_promotion_dryrun_receipt_stability_audit.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G45_ROUTE_PROMOTION_DRYRUN_RECEIPT_STABILITY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G45_ROUTE_PROMOTION_STABILITY_LEDGER.json`
- `specs/ASH_BASETRAIN_GPU_70K_G45_ROUTE_PROMOTION_DRYRUN_RECEIPT_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G45_ROUTE_PROMOTION_STABILITY_DIGEST_CONSISTENCY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G45_STABILITY_AUDIT_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G45_NO_DEFAULT_ADOPTION_SILENT_ADOPTION_LOSS_BACKWARD_OPTIMIZER_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G45_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G45_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G45_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G45_LOCAL_BAKE_VALIDATION.json`

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

## Allowed in G45 runtime probe

- Read G44 explicit route promotion dryrun receipt
- Read G44 route promotion execution candidate preflight
- Read G44 route promotion dryrun receipt boundary audit
- Read G43 route promotion execution candidate
- Check route promotion dryrun receipt, execution, and boundary acceptance
- Create route promotion dryrun receipt stability audit
- Create route promotion stability ledger
- Check route promotion stability digest consistency
- Validate state through lookup-table and match-based boundary classification
- Audit no-default-adoption, no-silent-adoption, no-loss, no-backward, and no-optimizer boundary

## Closed in G45

G45 must keep closed: route promotion dryrun rerun, route promotion execution, runtime default adoption, default route mutation, silent adoption, implicit route swap, production route switch, operator auto-approval, runtime route bind execution, final output emission, display surface writes, loss, backward, optimizer, model delta, checkpoint mutation, and weight mutation.

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G45_ROUTE_PROMOTION_DRYRUN_RECEIPT_STABILITY_AUDIT_READY_NO_LOCAL_ROUTE_PROMOTION_STABILITY_RUNTIME_CLAIM
```

The baked ZIP contains the G45 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G44 runtime PASS evidence were unavailable, so no local compile claim or route promotion dryrun receipt stability audit runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G45_ROUTE_PROMOTION_DRYRUN_RECEIPT_STABILITY_AUDIT
```

G45 reaches runtime PASS only when the G44 route promotion dryrun receipt, execution preflight, and dryrun receipt boundary are accepted, a stability audit is created, and a route promotion stability ledger is created as ledger-only while every closed boundary remains closed.

## Next

```text
ASH-BASETRAIN-GPU-70K-G46
Route Promotion Stability Ledger Operator Review Gate /
Route Promotion Stability Ledger To Explicit Promotion Execution Gate
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```
