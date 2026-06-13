# ASH-BASETRAIN-GPU-37R-R2 Acceptance Report

## Patch

```txt
ASH-BASETRAIN-GPU-37R-R2
Multi-Workgroup Reduction Receipt Source Rebind /
37Q-R1 PASS Receipt Locator No Placeholder Intake Seal
Readback Parity Gate Runtime Receipt Write Candidate
No Forward No Optimizer No Weight Mutation
```

## Status

```txt
STATIC_ACCEPTANCE = PASS
CARGO_BUILD = NOT_RUN_CARGO_UNAVAILABLE_IN_CONTAINER
RUNTIME_GPU = NOT_RUN_LOCAL_GPU_REQUIRED
```

## Implemented

- Rebound 37R patch identity to `ASH-BASETRAIN-GPU-37R-R2` while preserving `base_patch_id = ASH-BASETRAIN-GPU-37R`.
- Added `ASH-BASETRAIN-GPU-37Q-R1` as a supported upstream reduction receipt.
- Preserved legacy `ASH-BASETRAIN-GPU-37Q` intake compatibility.
- Accepted `PASS_ASH_BASETRAIN_GPU_37Q_R1*` status prefix.
- Split unsupported patch/status from JSON parse failure:
  - `BLOCKED_37Q_REDUCTION_RECEIPT_UNSUPPORTED_PATCH_ID`
  - `BLOCKED_37Q_REDUCTION_RECEIPT_UNSUPPORTED_STATUS`
- Added 37Q-R1 summary / partial matrix / source binding validation gates.
- Added R2 runtime artifact write path and legacy artifact write path.
- Preserved no-forward / no-optimizer / no-weight-mutation guards.

## Runtime Receipt Paths

```txt
artifacts/ASH_BASETRAIN_GPU_37R_R2_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_READBACK_PARITY_GATE.json
artifacts/ASH_BASETRAIN_GPU_37R_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_READBACK_PARITY_GATE.json
```

## Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_37r_selected_group_row_block_multi_workgroup_reduction_readback_parity_gate -- --reduction-receipt .\artifacts\ASH_BASETRAIN_GPU_37Q_R1_SELECTED_GROUP_ROW_BLOCK_MULTI_WORKGROUP_REDUCTION_DIAGNOSTIC_KERNEL.json
```

## Acceptance Expectation

Valid 37Q-R1 receipt should produce:

```txt
patch_id = ASH-BASETRAIN-GPU-37R-R2
verdict = PASS
pass = true
status starts_with PASS_ASH_BASETRAIN_GPU_37R_R2
source_binding.reduction_receipt_patch_id = ASH-BASETRAIN-GPU-37Q-R1
source_binding.reduction_receipt_supported_patch_id = true
source_binding.reduction_receipt_supported_status = true
reduction_parity_matrix.parity_passed = true
promotion_gate_matrix.forward_candidate_allowed_next = true
next_patch_if_pass = ASH-BASETRAIN-GPU-38
```

## Guard Contract

The patch must keep these false:

```txt
model_forward_executed
forward_output_adopted
logits_written
loss_computed
backward_executed
gradient_buffer_written
delta_candidate_written
optimizer_step_executed
weight_buffer_mutated
adapter_written
checkpoint_written
safetensors_written
```
