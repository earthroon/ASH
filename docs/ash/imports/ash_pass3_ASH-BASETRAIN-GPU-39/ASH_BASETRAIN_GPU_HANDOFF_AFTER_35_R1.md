# ASH BASETRAIN GPU handoff after 35-R1

## Latest patch

ASH-BASETRAIN-GPU-35-R1 — Selected Group Manifest Binding / Atlas Group Shape Byte Range Receipt / No Backward No Optimizer Seal.

## Default baked state

```txt
manifest_binding_status = BLOCKED_MISSING_MANIFEST_INPUT
manifest_bound_descriptor_ready = false
selected_group_gradient_buffer_allocated = false
runtime_gpu_buffer_created = false
selected_group_weights_loaded = false
backward_executed = false
optimizer_step_executed = false
```

## Operator env

```powershell
$env:ASH_BASETRAIN_GPU_SELECTED_GROUP_MANIFEST_PATH="D:\1111113232\DUST\1\ash_pass3\target\selected_atlas_group_slot_0_manifest.json"
```

## Next route

- If manifest-bound: ASH-BASETRAIN-GPU-36 — Selected Group Gradient Buffer Runtime Allocation Smoke / Manifest Bound Single Group Gradient Buffer No Backward No Optimizer Seal
- If blocked: ASH-BASETRAIN-GPU-35-R1A — Selected Group Manifest Binding Failure Triage / Missing Or Invalid Manifest Shape Byte Range Detail No Backward No Optimizer Seal
