# ASH-BASETRAIN-GPU-70K-G132-R1

## Receipt Boundary Scope Rebind

PatchId: `ASH-BASETRAIN-GPU-70K-G132-R1`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G131-R2A`  
PreviousBlockedTarget: `BLOCKED_ASH_BASETRAIN_GPU_70K_G132_EVIDENCE_BASELINE_INSUFFICIENT`  
PreviousBlockedVerdict: `BlockedForbiddenMutationClaim`

Seal: **No Backward / No Optimizer / No Weight Commit / No Checkpoint Mutation**

G132-R1 repairs the G132 receipt-boundary audit. G132 scanned the entire `specs/`, `docs/`, and `artifacts/` text surface and treated historical or example mutation strings as current G132 mutation claims.

G132-R1 narrows the receipt-boundary audit to the source patch family only:

```text
G131_R1 / G131-R1
G131_R2_B / G131-R2-B
G131_R2A / G131-R2A
```

The baked ZIP does not include generated artifacts. The Rust binary generates artifacts locally:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g132_r1_receipt_boundary_scope_rebind -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G131-R2A
```

PASS target:

```text
PASS_ASH_BASETRAIN_GPU_70K_G132_R1_RECEIPT_BOUNDARY_SCOPE_REBIND_NO_BACKWARD_NO_OPTIMIZER_NO_WEIGHT_COMMIT_NO_CHECKPOINT_MUTATION
```

Expected retained result:

```text
route_baseline_verdict=AtlasGroupedBackwardNotConnected
```

Expected repaired result:

```text
receipt_boundary_verdict=PASS_NO_FORBIDDEN_MUTATION_CLAIM_FOUND
```

Next patch: `ASH-BASETRAIN-GPU-70K-G133`.
