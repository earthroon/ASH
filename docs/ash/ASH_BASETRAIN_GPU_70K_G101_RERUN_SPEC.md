# ASH-BASETRAIN-GPU-70K-G101-RERUN

## Runtime Candidate Route Live Probe Re-evaluation

Seal: No Default Route Mutation / No Weight Commit / No Checkpoint Mutation

## Patch Identity

```text
PatchId: ASH-BASETRAIN-GPU-70K-G101-RERUN
SourcePatchId: ASH-BASETRAIN-GPU-70K-G100-BLOCKED
PreviousPassTarget: PASS_ASH_BASETRAIN_GPU_70K_G100_BLOCKED_RUNTIME_CANDIDATE_ROUTE_PROMOTION_BLOCK_LEDGER
RuntimePassTarget: PASS_ASH_BASETRAIN_GPU_70K_G101_RERUN_RUNTIME_CANDIDATE_ROUTE_LIVE_PROBE_RE_EVALUATION
NextPatch: ASH-BASETRAIN-GPU-70K-G102-RERUN-EXEC
```

G101-RERUN preserves the quarantined candidate and creates an adjusted probe policy plus recheck and rerun plans. It does not execute the live probe in this patch.

## Input SSOT

```text
ASH_BASETRAIN_GPU_70K_G100_BLOCKED_RUNTIME_CANDIDATE_ROUTE_PROMOTION_BLOCK_LEDGER_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G100_BLOCKED_PROMOTION_BLOCK_LEDGER.json
ASH_BASETRAIN_GPU_70K_G100_BLOCKED_REJECTED_CANDIDATE_QUARANTINE_STATE.json
ASH_BASETRAIN_GPU_70K_G100_BLOCKED_QUARANTINE_REVIEW_SEAL.json
ASH_BASETRAIN_GPU_70K_G100_BLOCKED_RECHECK_OR_DISCARD_DECISION_CANDIDATE.json
```

## Output SSOT

```text
ASH_BASETRAIN_GPU_70K_G101_RERUN_RUNTIME_CANDIDATE_ROUTE_LIVE_PROBE_RE_EVALUATION_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G101_RERUN_ADJUSTED_PROBE_POLICY.json
ASH_BASETRAIN_GPU_70K_G101_RERUN_QUARANTINED_CANDIDATE_RECHECK_PLAN.json
ASH_BASETRAIN_GPU_70K_G101_RERUN_LIVE_PROBE_PLAN.json
ASH_BASETRAIN_GPU_70K_G101_RERUN_BOUNDARY_AUDIT.json
```

## Opened State

```text
quarantined_candidate_recheck_created = true
adjusted_probe_policy_created = true
rerun_candidate_live_probe_plan_created = true
recheck_plan_created = true
```

## Closed State

```text
default_route_promotion_allowed_candidate = false
runtime_default_route_mutated = false
default_inference_pointer_mutated = false
production_route_mutated = false
actual_weight_mutated = false
actual_weight_committed = false
actual_checkpoint_mutated = false
promotion_applied_by_g101_rerun = false
live_probe_executed_by_g101_rerun = false
ledger_mutated_by_g101_rerun = false
```

## Cargo Surface

```rust
pub mod ash_basetrain_gpu_70k_g101_rerun_runtime_candidate_route_live_probe_re_evaluation;
```

```toml
[[bin]]
name = "ash_basetrain_gpu_70k_g101_rerun_runtime_candidate_route_live_probe_re_evaluation"
path = "src/bin/ash_basetrain_gpu_70k_g101_rerun_runtime_candidate_route_live_probe_re_evaluation.rs"
```

## PASS Target

```text
PASS_ASH_BASETRAIN_GPU_70K_G101_RERUN_RUNTIME_CANDIDATE_ROUTE_LIVE_PROBE_RE_EVALUATION
```
