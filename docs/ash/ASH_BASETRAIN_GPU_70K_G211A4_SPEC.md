# ASH-BASETRAIN-GPU-70K-G211A4

## TensorCube Applied Route CPU Reference Parity

PatchId: `ASH-BASETRAIN-GPU-70K-G211A4`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G211A3`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G211A5`  
Phase: `PhaseApplyA`

RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G211A4_TENSORCUBE_APPLIED_ROUTE_CPU_REFERENCE_PARITY_COMPARE_APPLIED_TENSORCUBE_RUNTIME_ROUTE_AGAINST_CPU_REFERENCE_RECEIPT_NO_SILENT_FALLBACK_NO_PRODUCTION_WEIGHT_MUTATION_NO_TENSORCORE_CLAIM`

## Purpose

G211A4 consumes the passed G211A3 TensorCube command submit execution receipt state.

G211A4 loads the applied TensorCube runtime route execution receipt and compares the applied route output against a CPU reference receipt.

G211A4 is the first apply-chain patch where `cpu_reference_parity_checked=true`.

G211A4 records an explicit TensorCube applied route parity audit and records a parity verdict as `Pass` or `Fail`.

G211A4 does not create the final apply verdict. Final apply verdict and rollback anchor are deferred to G211A5.

G211A4 does not mutate production weights, rewrite checkpoints, rewrite safetensors, replace production, claim benchmark improvement, claim model improvement, claim deployment, or claim TensorCore hardware acceleration.

## Core Boundary

```text
CPU reference parity != final apply verdict
parity Pass != production replacement
parity Fail != candidate deletion
applied route comparison != checkpoint rewrite
applied route comparison != safetensors mutation
execution receipt loaded != new command submit
CPU reference authority != benchmark claim
G211A4 != G211A5 final apply verdict
G211A4 != rollback execution
G211A4 != TensorCore hardware acceleration claim
```

## Source Load Contract

G211A4 must load and validate the G211A3 command submit execution receipt state.

Required G211A3 source artifacts:

```text
artifacts/g211a3/ASH_BASETRAIN_GPU_70K_G211A3_TENSORCUBE_COMMAND_SUBMIT_EXECUTION_RECEIPT.json
artifacts/g211a3/ASH_BASETRAIN_GPU_70K_G211A3_TENSORCUBE_RUNTIME_EXECUTION_PHASE_EVENTS.json
artifacts/g211a3/ASH_BASETRAIN_GPU_70K_G211A3_COMMAND_ENCODER_SUBMIT_RECEIPT.json
artifacts/g211a3/ASH_BASETRAIN_GPU_70K_G211A3_COMPUTE_DISPATCH_RECEIPT.json
artifacts/g211a3/ASH_BASETRAIN_GPU_70K_G211A3_NO_CPU_PARITY_VERDICT_SEAL.json
artifacts/g211a3/ASH_BASETRAIN_GPU_70K_G211A3_NO_PRODUCTION_REPLACEMENT_SEAL.json
artifacts/g211a3/ASH_BASETRAIN_GPU_70K_G211A3_NO_SILENT_FALLBACK_SEAL.json
artifacts/g211a3/ASH_BASETRAIN_GPU_70K_G211A3_NO_PRODUCTION_WEIGHT_MUTATION_SEAL.json
artifacts/g211a3/ASH_BASETRAIN_GPU_70K_G211A3_G211A4_ENTRY_PACKET.json
artifacts/g211a3/PASS_ASH_BASETRAIN_GPU_70K_G211A3.txt
```

## Required Runtime States

```text
cpu_reference_parity_phase_entered=true
cpu_reference_parity_phase=PhaseApplyACpuReferenceParity

tensorcube_runtime_execution_receipt_loaded=true
tensorcube_runtime_execution_phase_events_loaded=true
command_encoder_submit_receipt_loaded=true
compute_dispatch_receipt_loaded=true

cpu_reference_loaded=true
cpu_reference_receipt_status=Created
cpu_reference_mode=DeterministicScalarReference
cpu_reference_input_fixture_status=Loaded
cpu_reference_expected_output_status=Created

applied_route_output_loaded=true
applied_route_output_status=LoadedFromG211A3ExecutionReceipt
applied_route_output_source=G211A3TensorCubeRuntimeExecutionReceipt

applied_route_cpu_reference_comparison_status=Audited
applied_route_cpu_reference_comparison_mode=AbsRelToleranceComparison
applied_route_cpu_reference_comparison_receipt_status=Created

shape_check_performed=true
shape_match=true
shape_mismatch_detected=false
nan_inf_check_performed=true
nan_inf_detected=false
tolerance_check_performed=true
abs_tolerance_applied=true
rel_tolerance_applied=true
within_tolerance=true

cpu_reference_parity_checked=true
cpu_reference_parity_status=Audited
parity_verdict=Pass

candidate_route_released=true
candidate_route_staged_for_runtime=true
candidate_route_bound_live=true
runtime_route_enabled=true
command_encoder_submitted=true
compute_dispatch_performed=true
tensorcube_runtime_execution_receipt_status=Created

new_command_encoder_submitted=false
new_compute_dispatch_performed=false
runtime_execution_replayed=false
runtime_execution_replay_required=false

silent_fallback_allowed=false
silent_fallback_detected=false
production_weight_mutation_allowed=false
production_base_weight_mutated=false
checkpoint_rewritten=false
safetensors_rewritten=false
optimizer_state_mutated=false
training_weight_mutated=false
production_replacement_executed=false
tensorcore_hardware_acceleration_claimed=false
benchmark_claimed=false
model_improvement_claimed=false
deployment_claimed=false

final_apply_verdict_recorded=false
rollback_anchor_created=false

g211a5_entry_packet_status=Created
g211a5_entry_packet_target=ASH-BASETRAIN-GPU-70K-G211A5
ready_for_g211a5=true
```

## Expected Runtime Artifacts

Runtime artifacts are not prebaked into this ZIP. Rust must create them locally at run time.

```text
artifacts/g211a4/ASH_BASETRAIN_GPU_70K_G211A4_TENSORCUBE_APPLIED_ROUTE_CPU_REFERENCE_PARITY_RECEIPT.json
artifacts/g211a4/ASH_BASETRAIN_GPU_70K_G211A4_CPU_REFERENCE_RECEIPT.json
artifacts/g211a4/ASH_BASETRAIN_GPU_70K_G211A4_APPLIED_ROUTE_OUTPUT_RECEIPT.json
artifacts/g211a4/ASH_BASETRAIN_GPU_70K_G211A4_PARITY_COMPARISON_RECEIPT.json
artifacts/g211a4/ASH_BASETRAIN_GPU_70K_G211A4_PARITY_VERDICT.json
artifacts/g211a4/ASH_BASETRAIN_GPU_70K_G211A4_NO_FINAL_APPLY_VERDICT_SEAL.json
artifacts/g211a4/ASH_BASETRAIN_GPU_70K_G211A4_NO_PRODUCTION_REPLACEMENT_SEAL.json
artifacts/g211a4/ASH_BASETRAIN_GPU_70K_G211A4_NO_SILENT_FALLBACK_SEAL.json
artifacts/g211a4/ASH_BASETRAIN_GPU_70K_G211A4_NO_PRODUCTION_WEIGHT_MUTATION_SEAL.json
artifacts/g211a4/ASH_BASETRAIN_GPU_70K_G211A4_G211A5_ENTRY_PACKET.json
artifacts/g211a4/PASS_ASH_BASETRAIN_GPU_70K_G211A4.txt
```

## Acceptance Criteria

```text
G211A3 PASS marker is loaded.
G211A3 TensorCube command submit execution receipt is loaded.
G211A3 runtime execution phase events are loaded.
G211A3 command encoder submit receipt is loaded.
G211A3 compute dispatch receipt is loaded.
G211A3 no CPU parity verdict seal is loaded as prior state.
G211A3 no production replacement seal is loaded.
G211A3 no silent fallback seal is loaded.
G211A3 no production weight mutation seal is loaded.
G211A3 G211A4 entry packet is loaded.
source_command_encoder_submitted=true.
source_compute_dispatch_performed=true.
source_tensorcube_runtime_execution_receipt_status=Created.
source_cpu_reference_parity_checked=false.
source_cpu_reference_parity_status=DeferredToG211A4.
source_parity_verdict=NotEvaluatedInG211A3.
source_ready_for_g211a4=true.
tensorcube_runtime_execution_receipt_loaded=true.
cpu_reference_loaded=true.
cpu_reference_receipt_status=Created.
applied_route_output_loaded=true.
applied_route_cpu_reference_comparison_status=Audited.
shape_check_performed=true.
nan_inf_check_performed=true.
tolerance_check_performed=true.
cpu_reference_parity_checked=true.
cpu_reference_parity_status=Audited.
parity_verdict is Pass or Fail.
final_apply_verdict_recorded=false.
rollback_anchor_created=false.
G211A5 entry packet is ready.
```

## Runtime

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211a4_applied_route_cpu_reference_parity.rs
```

## Cargo Run Command

```bash
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211a4_applied_route_cpu_reference_parity
```

## Next Patch

`ASH-BASETRAIN-GPU-70K-G211A5`

```text
TensorCube Apply Verdict And Rollback Anchor /
Record Final Apply Verdict With Explicit Rollback Anchor /
No Silent Fallback No Production Weight Mutation No TensorCore Claim
```
