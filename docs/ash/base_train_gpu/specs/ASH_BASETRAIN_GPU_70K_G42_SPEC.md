# ASH-BASETRAIN-GPU-70K-G42 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G42
Promotion Dryrun Receipt Stability Audit /
Dryrun Receipt To Promotion Stability Ledger
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```

## Purpose

G42 consumes the `ASH-BASETRAIN-GPU-70K-G41` promotion dryrun receipt and creates two receipt-only outputs:

1. promotion dryrun receipt stability audit
2. promotion stability ledger

G42 audits and ledgers the already-created dryrun receipt. It does not rerun the dryrun and does not promote the route.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent route promotion candidate: `ASH-BASETRAIN-GPU-70K-G39`
- Parent promotion dryrun candidate: `ASH-BASETRAIN-GPU-70K-G40`
- Parent promotion dryrun receipt: `ASH-BASETRAIN-GPU-70K-G41`
- Current patch: `ASH-BASETRAIN-GPU-70K-G42`
- Next patch: `ASH-BASETRAIN-GPU-70K-G43`

## Implementation style

G42 is baked in a lookup-table-first and match-based boundary style.

- `EXPECTED_STATE_LUT` holds the expected truth table.
- `G42ProbeKey` enumerates the boundary fields.
- `expected_value(...)` uses `match` for expected state lookup.
- `classify_boundary(...)` uses `match` to map observed mismatches to `G42FailureReason`.
- Forbidden callsite patterns are kept in static receipt JSON, not in source, to prevent source self-hit contamination.

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g42_promotion_dryrun_receipt_stability_audit.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g42_promotion_dryrun_receipt_stability_audit.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G42_PROMOTION_DRYRUN_RECEIPT_STABILITY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G42_PROMOTION_STABILITY_LEDGER.json`
- `specs/ASH_BASETRAIN_GPU_70K_G42_PROMOTION_DRYRUN_RECEIPT_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G42_PROMOTION_STABILITY_DIGEST_CONSISTENCY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G42_STABILITY_AUDIT_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G42_NO_DEFAULT_ADOPTION_SILENT_ADOPTION_LOSS_BACKWARD_OPTIMIZER_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G42_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G42_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G42_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G42_LOCAL_BAKE_VALIDATION.json`

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

## Allowed in G42 runtime probe

- Read G41 promotion dryrun execution receipt
- Read G41 promotion dryrun receipt
- Read G41 promotion dryrun receipt boundary audit
- Read G40 explicit promotion dryrun candidate
- Check receipt, execution, and boundary acceptance
- Create promotion dryrun receipt stability audit
- Create promotion stability ledger
- Check promotion stability digest consistency
- Audit no-default-adoption, no-silent-adoption, no-loss, no-backward, and no-optimizer boundary

## Closed in G42

G42 must keep closed: dryrun rerun, route promotion execution, runtime default adoption, default route mutation, silent adoption, implicit route swap, production route switch, operator auto-approval, runtime route bind execution, final output emission, display surface writes, loss, backward, optimizer, model delta, checkpoint mutation, and weight mutation.

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G42_PROMOTION_DRYRUN_RECEIPT_STABILITY_AUDIT_READY_NO_LOCAL_PROMOTION_STABILITY_RUNTIME_CLAIM
```

The baked ZIP contains the G42 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G41 runtime PASS evidence were unavailable, so no local compile claim or promotion dryrun receipt stability audit runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G42_PROMOTION_DRYRUN_RECEIPT_STABILITY_AUDIT
```

G42 reaches runtime PASS only when the G41 promotion dryrun receipt and execution receipt are accepted, the dryrun receipt boundary is accepted, a stability audit is created, and a promotion stability ledger is created as ledger-only while every closed boundary remains closed.

## Next

```text
ASH-BASETRAIN-GPU-70K-G43
Promotion Stability Ledger Operator Review Gate /
Promotion Stability Ledger To Route Promotion Execution Candidate
No Default Adoption No Silent Adoption No Loss No Backward No Optimizer
```
