# ASH-BASETRAIN-GPU-70K-G151

## Active Runtime Route Forward Stability Gate

PatchId: `ASH-BASETRAIN-GPU-70K-G151`
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G150`
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G151_ACTIVE_RUNTIME_ROUTE_FORWARD_STABILITY_GATE_REPEATED_FORWARD_SMOKE_DETERMINISM_NO_PRODUCTION_COMPLETION_CLAIM`

G151 repeats the G150 active runtime forward smoke probe and records stability evidence. It checks repeated output digest stability, route binding stability, and active-runtime-only execution. It remains a stability receipt stage only.

## CLI

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g151_active_runtime_route_forward_stability_gate -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G150 `
  --stability-mode repeated-forward-smoke `
  --repeat-count 3
```

## Input SSOT

```text
ASH_BASETRAIN_GPU_70K_G150_ACTIVE_RUNTIME_ROUTE_SMOKE_INFERENCE_GATE_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G150_FORWARD_SMOKE_PROBE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G150_FORWARD_OUTPUT_DIGEST_AUDIT.json
ASH_BASETRAIN_GPU_70K_G150_FORWARD_ROUTE_BINDING_AUDIT.json
ASH_BASETRAIN_GPU_70K_G150_PRODUCTION_COMPLETION_CLAIM_BLOCK_AUDIT.json
```

## Expected PASS summary

```text
previous_g150_accepted=true
active_runtime_route_created=true
runtime_route_promoted=true
active_runtime_forward_smoke_verified=true
stability_mode=RepeatedForwardSmoke
repeat_count=3
repeated_forward_smoke_attempted=true
repeated_forward_smoke_executed=true
repeated_forward_smoke_succeeded=true
all_repeat_digests_recorded=true
forward_output_digest_stable=true
forward_output_digest_nonempty=true
forward_output_nan_detected=false
forward_output_inf_detected=false
forward_route_binding_stable=true
forward_used_active_runtime_route=true
forward_used_production_route=false
forward_smoke_determinism_verified=true
production_route_promoted=false
production_completion_claimed=false
training_completion_claimed=false
optimizer_step_executed_in_g151=false
backward_executed_in_g151=false
gradient_mutated_in_g151=false
forward_stability_verdict=RepeatedForwardSmokeDeterminismVerifiedNoProductionCompletionClaim
output_files_written=8
```

## Next patch

`ASH-BASETRAIN-GPU-70K-G152` should review stability evidence for production-route candidacy while keeping production completion separate.
