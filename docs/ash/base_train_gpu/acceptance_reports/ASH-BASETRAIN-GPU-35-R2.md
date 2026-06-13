# ASH-BASETRAIN-GPU-35-R2 Acceptance

Default baked route is blocked safe because no operator manifest is provided in container. No shape/dtype/byte range was invented.

Expected blocked verdict:

```txt
PASS_ASH_BASETRAIN_GPU_35_R2_SELECTED_GROUP_MANIFEST_TEMPLATE_MATERIALIZATION_BLOCKED_SAFE_NO_INVENTED_SHAPE_NO_BACKWARD_NO_OPTIMIZER
```

Expected materialized verdict when operator manifest validates:

```txt
PASS_ASH_BASETRAIN_GPU_35_R2_SELECTED_GROUP_MANIFEST_TEMPLATE_MATERIALIZATION_OPERATOR_PROVIDED_ATLAS_GROUP_SHAPE_BYTE_RANGE_MANIFEST_RECEIPT_NO_BACKWARD_NO_OPTIMIZER
```
