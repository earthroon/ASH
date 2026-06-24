# ASH-BASETRAIN-GPU-70K-G143-R1

## Forbidden Real Commit Scanner Scope Rebind

PatchId: `ASH-BASETRAIN-GPU-70K-G143-R1`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G143`  
PreviousBlockedTarget: `BLOCKED_ASH_BASETRAIN_GPU_70K_G143_COMMIT_PERMISSION_QUARANTINE_GATE_INSUFFICIENT`  
PreviousBlockedVerdict: `BlockedForbiddenRealCommitCallDetected`

Seal: **Queue Write Buffer Context Split / Runtime Commit Surface Only / No Base Weight Commit / No Checkpoint Mutation**

G143-R1 fixes the G143 forbidden real commit scanner. G143 previously scanned the broader `crates/base_train/src` tree and treated normal GPU upload/forward/diagnostic `queue.write_buffer(` calls as forbidden real commit calls. The uploaded G143 forbidden audit showed no actual base mutation, no checkpoint mutation, no real base commit, and no commit permission grant. The block came from scanner scope and pattern policy.

## Intent

G143-R1 keeps G143 isolated commit dry-run semantics unchanged. It only rebinds scanner scope and queue write classification.

## Scope rebind

The forbidden scanner must inspect only the G143 runtime commit surface:

```text
crates/base_train/src/ash_basetrain_gpu_70k_g143_commit_permission_quarantine_gate.rs
crates/base_train/src/bin/ash_basetrain_gpu_70k_g143_commit_permission_quarantine_gate.rs
```

It must not recursively scan all of `crates/base_train/src`.

## Queue write buffer split

`queue.write_buffer(` is removed from hard forbidden real commit patterns.

Reason:

```text
queue.write_buffer( is a normal WebGPU upload verb used by upload, forward, readback, diagnostic, and dispatch smoke stages.
It is not sufficient evidence of base weight commit.
```

If encountered outside commit surface context, it must be ignored or labeled as non-commit GPU upload context rather than hard-blocked.

## Hard forbidden patterns retained

```text
commit_permission_granted=true
commit_execution_allowed=true
commit_execution_executed=true
real_base_commit_executed=true
candidate_delta.apply_to_base
commit_candidate_delta(
promote_candidate_delta(
base_weights.copy_from
base_weights.copy_
base_weights.assign
base_weights.set_data
module.set_weight
model.set_weight
save_checkpoint(
write_safetensors(
runtime_route_promote(
production_route_promote(
training_completion_claimed=true
```

## Audit behavior

`ASH_BASETRAIN_GPU_70K_G143_FORBIDDEN_REAL_COMMIT_AUDIT.json` may include:

```json
{
  "scan_scope": "G143RuntimeCommitSurfaceOnly",
  "checked_files": [
    "crates/base_train/src/ash_basetrain_gpu_70k_g143_commit_permission_quarantine_gate.rs",
    "crates/base_train/src/bin/ash_basetrain_gpu_70k_g143_commit_permission_quarantine_gate.rs"
  ],
  "forbidden_real_commit_hits": [],
  "ignored_real_commit_hits": []
}
```

## Expected rerun result

Rerunning the existing G143 binary after R1 should allow isolated dry run creation and produce:

```text
PASS_ASH_BASETRAIN_GPU_70K_G143_COMMIT_PERMISSION_QUARANTINE_GATE_NO_BASE_WEIGHT_COMMIT_NO_CHECKPOINT_MUTATION
verdict=Pass
previous_g142_accepted=true
approval_receipt_bound_to_review_item=true
commit_permission_candidate_created=true
commit_permission_granted=false
isolated_commit_dry_run_state_created=true
isolated_commit_dry_run_executed=true
isolated_commit_dry_run_observed=true
candidate_delta_applied_in_isolated_state=true
candidate_delta_applied_to_base=false
real_base_commit_executed=false
base_weight_digest_unchanged=true
actual_base_weight_mutated=false
checkpoint_written=false
checkpoint_mutated=false
runtime_route_promoted=false
training_completion_claimed=false
commit_quarantine_verdict=CommitPermissionQuarantinedDryRunNoBaseCommit
output_files_written=8
```

## Non-goals

G143-R1 does not perform a real commit, does not grant commit permission, does not mutate base weights, does not write checkpoints, and does not promote a runtime route.

## Next patch

`ASH-BASETRAIN-GPU-70K-G144` should review the isolated commit dry-run result and create a commit permission review packet. It must still avoid real base weight commit and checkpoint mutation.
