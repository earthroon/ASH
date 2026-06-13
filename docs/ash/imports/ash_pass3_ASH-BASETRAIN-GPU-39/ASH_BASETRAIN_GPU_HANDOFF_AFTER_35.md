# ASH-BASETRAIN-GPU-35 Handoff

## Status

- Patch: `ASH-BASETRAIN-GPU-35`
- Title: `Selected Group Gradient Buffer Allocation Candidate / Single Atlas Group Gradient Buffer Contract No Backward No Optimizer Seal`
- Expected verdict: `PASS_ASH_BASETRAIN_GPU_35_SELECTED_GROUP_GRADIENT_BUFFER_ALLOCATION_CANDIDATE_SINGLE_ATLAS_GROUP_GRADIENT_BUFFER_CONTRACT_NO_BACKWARD_NO_OPTIMIZER`
- Default no-manifest route: `ASH-BASETRAIN-GPU-35-R1_SELECTED_GROUP_MANIFEST_BINDING_NO_BACKWARD_NO_OPTIMIZER`
- Manifest-bound route: `ASH-BASETRAIN-GPU-36_SELECTED_GROUP_GRADIENT_BUFFER_RUNTIME_ALLOCATION_SMOKE_NO_BACKWARD_NO_OPTIMIZER`

## SSOT

Source confirmed PASS is `ASH-BASETRAIN-GPU-34`.

34 opened only a contract-only single selected atlas group scope. It did not load selected group weights, did not create a gradient buffer, did not compute model weight gradients, and did not execute backward or optimizer.

## 35 Boundary

35 creates a selected group gradient buffer allocation candidate contract.
It does not perform actual GPU allocation by default.
It does not infer missing manifest, tensor shape, dtype, element count, or byte ranges.

## Default Current Result

No manifest is bundled by default, so local default execution should produce:

```txt
allocation_candidate_status = BLOCKED_MISSING_SELECTED_GROUP_MANIFEST
blocked_candidate_is_safe = true
selected_group_gradient_buffer_allocated = false
model_weight_gradient_computed = false
backward_executed = false
```

## Optional Manifest Gate

Set the optional env var to test manifest-bound descriptor mode:

```powershell
$env:ASH_BASETRAIN_GPU_SELECTED_GROUP_MANIFEST_PATH="D:\1111113232\DUST\1\ash_pass3\target\selected_atlas_group_slot_0_manifest.json"
```

Required manifest keys for descriptor-finalized route:

```txt
selected_group_tensor_shape
selected_group_dtype
selected_group_element_count
selected_group_weight_byte_start
selected_group_weight_byte_end
selected_group_weight_byte_len
```

## Next

If blocked by missing manifest, continue with:

```txt
ASH-BASETRAIN-GPU-35-R1
Selected Group Manifest Binding /
Atlas Group Shape Byte Range Receipt No Backward No Optimizer Seal
```

If manifest-bound descriptor is created, continue with:

```txt
ASH-BASETRAIN-GPU-36
Selected Group Gradient Buffer Runtime Allocation Smoke /
Manifest Bound Single Group Gradient Buffer No Backward No Optimizer Seal
```
