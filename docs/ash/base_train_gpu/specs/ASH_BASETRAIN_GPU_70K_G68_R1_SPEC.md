# ASH-BASETRAIN-GPU-70K-G68-R1

Patch: ASH-BASETRAIN-GPU-70K-G68-R1
Title: Dispatch Submit Candidate Lineage Continuity Hotfix

Status: source-baked specification record.

Source files:
- crates/base_train/src/lib.rs
- crates/base_train/src/ash_basetrain_gpu_70k_g68_r1_dispatch_submit_candidate_lineage_continuity_hotfix.rs
- crates/base_train/src/bin/ash_basetrain_gpu_70k_g68_r1_dispatch_submit_candidate_lineage_continuity_hotfix.rs

Required lib registration:

```rust
pub mod ash_basetrain_gpu_70k_g68_r1_dispatch_submit_candidate_lineage_continuity_hotfix;
```

PASS target:

PASS_ASH_BASETRAIN_GPU_70K_G68_R1_DISPATCH_SUBMIT_CANDIDATE_LINEAGE_CONTINUITY_HOTFIX

Purpose:
- Preserve G68 runtime PASS semantics.
- Carry forward explicit_permission_grant_candidate_digest from the G65/G66 lineage into the G68 dispatch submit candidate receipts.
- Repair only lineage metadata.
- Do not perform command queue submit, dispatch submit, backward execution, gradient write, optimizer, weight mutation, or checkpoint mutation.

Packaging note: G68-R1 bake includes lib.rs registration, Cargo bin registration, proactive path-mod bin hotfix, recursion limit, and excludes predecessor runtime receipts for G50 through G68.
