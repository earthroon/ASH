# ASH BASETRAIN GPU handoff after 35-R1A

## Latest patch

ASH-BASETRAIN-GPU-35-R1A — Selected Group Manifest Binding Failure Triage / Missing Or Invalid Manifest Shape Byte Range Detail / No Backward No Optimizer Seal.

## Current state

```txt
manifest_failure_triage_created = true
manifest_binding_status = BLOCKED_MISSING_MANIFEST_INPUT
operator_manifest_template_written = true
manifest_bound_descriptor_ready = false
selected_group_gradient_buffer_allocated = false
runtime_gpu_buffer_created = false
backward_executed = false
optimizer_step_executed = false
```

## Operator template

```txt
target/selected_atlas_group_slot_0_manifest.template.json
```

Template null fields are placeholders. They are not valid shape/dtype/byte-range values.

## Next route

ASH-BASETRAIN-GPU-35-R2 — Selected Group Manifest Template Materialization / Operator Provided Atlas Group Shape Byte Range Manifest Receipt / No Backward No Optimizer Seal.
