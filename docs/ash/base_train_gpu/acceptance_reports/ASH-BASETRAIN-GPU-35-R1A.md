# ASH-BASETRAIN-GPU-35-R1A Acceptance Report

## Verdict

```txt
PASS_ASH_BASETRAIN_GPU_35_R1A_SELECTED_GROUP_MANIFEST_BINDING_FAILURE_TRIAGE_MISSING_OR_INVALID_MANIFEST_SHAPE_BYTE_RANGE_DETAIL_NO_BACKWARD_NO_OPTIMIZER
```

## Default baked route

```txt
manifest_binding_status = BLOCKED_MISSING_MANIFEST_INPUT
manifest_failure_triage_created = true
operator_manifest_template_written = true
manifest_bound_descriptor_ready = false
selected_group_gradient_buffer_allocated = false
runtime_gpu_buffer_created = false
backward_executed = false
optimizer_step_executed = false
```

## Template

`target/selected_atlas_group_slot_0_manifest.template.json` contains null placeholders only; it is not a manifest-bound descriptor.
