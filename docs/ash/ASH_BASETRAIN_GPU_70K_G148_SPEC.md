# ASH-BASETRAIN-GPU-70K-G148

## Verified Checkpoint Runtime Route Candidate Gate

PatchId: `ASH-BASETRAIN-GPU-70K-G148`
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G147`
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G148_VERIFIED_CHECKPOINT_RUNTIME_ROUTE_CANDIDATE_GATE_NO_PRODUCTION_ROUTE_PROMOTION`

G148 creates a runtime route candidate from the G147 readback verified checkpoint. It does not promote the active runtime route, production route, default inference route, or training completion state.

## CLI

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g148_verified_checkpoint_runtime_route_candidate_gate -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G147 `
  --route-mode runtime-candidate
```

## Input SSOT

```text
ASH_BASETRAIN_GPU_70K_G147_CHECKPOINT_CANDIDATE_INTEGRITY_REPLAY_GATE_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G147_CHECKPOINT_READBACK_AUDIT.json
ASH_BASETRAIN_GPU_70K_G147_CHECKPOINT_DIGEST_REPLAY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G147_CHECKPOINT_SCOPE_BINDING_AUDIT.json
```

## Expected PASS summary

```text
verdict=Pass
previous_g147_accepted=true
checkpoint_candidate_integrity_verified=true
checkpoint_readback_digest_matches_candidate=true
checkpoint_readback_digest_bound_to_base_commit=true
checkpoint_scope_binding_verified=true
route_mode=RuntimeCandidate
runtime_route_candidate_created=true
runtime_route_candidate_descriptor_created=true
runtime_route_candidate_digest_recorded=true
runtime_route_candidate_digest_bound=true
runtime_route_candidate_bound_to_checkpoint_readback=true
runtime_route_candidate_bound_to_base_commit=true
runtime_route_candidate_ready=true
ready_for_runtime_route_promotion_review=true
runtime_route_promoted=false
production_route_promoted=false
route_pointer_switched=false
default_inference_route_changed=false
training_completion_claimed=false
checkpoint_rewritten_in_g148=false
safetensors_rewritten_in_g148=false
unrelated_weight_mutation_detected=false
runtime_route_candidate_verdict=RuntimeRouteCandidateCreatedNoProductionPromotion
output_files_written=8
```

## Next patch

`ASH-BASETRAIN-GPU-70K-G149` should activate the runtime route candidate as active runtime route while keeping production promotion separate.
