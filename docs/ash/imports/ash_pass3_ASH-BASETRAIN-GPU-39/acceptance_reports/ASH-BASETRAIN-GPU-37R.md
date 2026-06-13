# ASH-BASETRAIN-GPU-37R Acceptance Report

## Patch

ASH-BASETRAIN-GPU-37R
Selected Group Row Block Multi-Workgroup Reduction Readback Parity Gate / Diagnostic Reduction Result To CPU Reference Seal / No Forward Adoption No Optimizer No Weight Mutation

## Scope

This patch adds a readback parity gate for the selected group row-block multi-workgroup diagnostic reduction result produced by ASH-BASETRAIN-GPU-37Q.

## Contract

- Intake a 37Q reduction receipt by `--reduction-receipt`.
- Require 37Q PASS.
- Require 37Q GPU dispatch and readback to be executed.
- Require no forward adoption, no optimizer execution, and no weight mutation.
- Compare GPU diagnostic readback words against CPU reference words encoded in the 37Q partial match matrix.
- Seal exact `u32` diagnostic word parity because 37Q uses raw f32-bitcast-to-u32 diagnostic arithmetic, not f32 numeric reduction.
- Produce a promotion gate receipt for moving to ASH-BASETRAIN-GPU-38 only when parity passes.

## Not Allowed

- No model forward execution.
- No logits write.
- No loss compute.
- No backward.
- No optimizer.
- No gradient write.
- No weight mutation.
- No safetensors write.
- No checkpoint write.
- No silent tolerance widening.

## Expected PASS Status

```text
PASS_ASH_BASETRAIN_GPU_37R_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_READBACK_PARITY_GATE_DIAGNOSTIC_REDUCTION_RESULT_TO_CPU_REFERENCE_SEAL_NO_FORWARD_NO_OPTIMIZER_NO_WEIGHT_MUTATION
```

## Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_37r_selected_group_row_block_multi_workgroup_reduction_readback_parity_gate -- --reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37Q_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_DIAGNOSTIC_KERNEL.json
```
