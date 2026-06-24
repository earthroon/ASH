# ASH-BASETRAIN-GPU-70K-G147

## Checkpoint Candidate Integrity Replay Gate

PatchId: `ASH-BASETRAIN-GPU-70K-G147`
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G146`
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G147_CHECKPOINT_CANDIDATE_INTEGRITY_REPLAY_GATE_READBACK_VERIFIED_NO_RUNTIME_ROUTE_PROMOTION`

G147 verifies the G146 written checkpoint candidate by readback. It creates readback verification artifacts only. It does not rewrite checkpoint data and does not promote runtime route.

## CLI

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g147_checkpoint_candidate_integrity_replay_gate -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G146 `
  --readback-mode verify-candidate
```

## Input SSOT

```text
ASH_BASETRAIN_GPU_70K_G146_POST_COMMIT_CHECKPOINT_FINALIZE_GATE_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G146_CHECKPOINT_WRITE_CANDIDATE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G146_CHECKPOINT_DIGEST_CANDIDATE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G146_CHECKPOINT_FINALIZE_RECEIPT.json
```

## Expected PASS summary

```text
verdict=Pass
previous_g146_accepted=true
checkpoint_write_candidate_materialized=true
checkpoint_candidate_scope=CommittedBaseWeightState
checkpoint_digest_candidate_recorded=true
checkpoint_digest_candidate_bound_to_base_commit=true
checkpoint_digest_matches_committed_base_scope=true
readback_mode=VerifyCandidate
checkpoint_candidate_readback_attempted=true
checkpoint_candidate_readback_succeeded=true
checkpoint_readback_digest_recorded=true
checkpoint_readback_digest_matches_candidate=true
checkpoint_readback_digest_bound_to_base_commit=true
checkpoint_scope_binding_verified=true
checkpoint_candidate_integrity_verified=true
checkpoint_rewritten_in_g147=false
checkpoint_mutated_in_g147=false
safetensors_rewritten_in_g147=false
runtime_route_promoted=false
production_route_promoted=false
route_pointer_switched=false
default_inference_route_changed=false
training_completion_claimed=false
checkpoint_replay_verdict=CheckpointCandidateReadbackVerifiedNoRuntimePromotion
output_files_written=8
```

## Next patch

`ASH-BASETRAIN-GPU-70K-G148` should prepare a runtime route candidate from the readback verified checkpoint while keeping production promotion separate.
