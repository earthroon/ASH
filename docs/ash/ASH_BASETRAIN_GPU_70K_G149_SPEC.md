# ASH-BASETRAIN-GPU-70K-G149

## Runtime Route Candidate Activation Gate

PatchId: `ASH-BASETRAIN-GPU-70K-G149`
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G148`
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G149_RUNTIME_ROUTE_CANDIDATE_ACTIVATION_GATE_ACTIVE_RUNTIME_ROUTE_NO_PRODUCTION_ROUTE_PROMOTION`

G149 activates the G148 runtime route candidate as an active runtime route. It allows active runtime route creation only. It does not promote production route, switch default inference route, or claim training completion.

## CLI

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g149_runtime_route_candidate_activation_gate -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G148 `
  --activation-mode active-runtime
```

## Input SSOT

```text
ASH_BASETRAIN_GPU_70K_G148_VERIFIED_CHECKPOINT_RUNTIME_ROUTE_CANDIDATE_GATE_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G148_RUNTIME_ROUTE_CANDIDATE_DESCRIPTOR.json
ASH_BASETRAIN_GPU_70K_G148_RUNTIME_ROUTE_CANDIDATE_DIGEST_BINDING_AUDIT.json
ASH_BASETRAIN_GPU_70K_G148_RUNTIME_ROUTE_CANDIDATE_READINESS_AUDIT.json
```

## Expected PASS summary

```text
verdict=Pass
previous_g148_accepted=true
runtime_route_candidate_created=true
runtime_route_candidate_digest_bound=true
runtime_route_candidate_ready=true
activation_mode=ActiveRuntime
active_runtime_route_created=true
active_runtime_route_descriptor_created=true
active_runtime_route_digest_recorded=true
active_runtime_route_digest_bound=true
active_runtime_route_bound_to_runtime_candidate=true
active_runtime_route_bound_to_checkpoint_readback=true
active_runtime_route_bound_to_base_commit=true
runtime_candidate_promoted_to_active=true
runtime_route_promoted=true
runtime_route_activation_scope=ActiveRuntimeOnly
active_runtime_route_ready=true
ready_for_production_route_promotion_review=true
production_route_promoted=false
production_route_pointer_switched=false
default_inference_route_changed=false
training_completion_claimed=false
checkpoint_rewritten_in_g149=false
safetensors_rewritten_in_g149=false
base_weight_mutated_in_g149=false
unrelated_weight_mutation_detected=false
active_runtime_route_verdict=ActiveRuntimeRouteCreatedNoProductionPromotion
output_files_written=8
```

## Next patch

`ASH-BASETRAIN-GPU-70K-G150` should run a forward smoke probe through the active runtime route while keeping production completion claim separate.
