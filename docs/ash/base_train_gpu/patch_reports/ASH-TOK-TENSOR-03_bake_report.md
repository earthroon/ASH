# ASH-TOK-TENSOR-03 Bake Report

## Patch

```txt
ASH-TOK-TENSOR-03
Atlas Parallel Grouped Sequential Tensor Load Plan / No Full Checkpoint Upload Seal
```

## Baked Files

```txt
crates/model_core/src/ash_tok_tensor_03_atlas_grouped_sequential_tensor_load_plan.rs
crates/model_core/src/bin/ash_tok_tensor_03_atlas_grouped_sequential_tensor_load_plan.rs
crates/model_core/src/lib.rs
crates/model_core/Cargo.toml
acceptance_reports/ASH-TOK-TENSOR-03.md
patch_reports/ASH-TOK-TENSOR-03_bake_report.md
ASH_TOK_TENSOR_03_TENSOR_GROUP_MANIFEST.json
ASH_TOK_TENSOR_03_ATLAS_GROUP_PLAN.json
ASH_TOK_TENSOR_03_SEQUENTIAL_LOAD_PLAN.json
ASH_TOK_TENSOR_03_GROUP_ORDER_RECEIPT.json
ASH_TOK_TENSOR_03_STATIC_CHECKS.txt
ASH_TOK_TENSOR_03_BAKE_MANIFEST.json
ASH_TOK_TENSOR_03_LOCAL_VALIDATION.txt
```

## Execution Boundary

```txt
safetensors read = not executed
SafeTensors deserialize = not executed
full checkpoint upload = not executed
model forward = not executed
optimizer step = not executed
weight commit = not executed
```

## Verdict

```txt
PASS_ASH_TOK_TENSOR_03_ATLAS_PARALLEL_GROUPED_SEQUENTIAL_TENSOR_LOAD_PLAN_NO_FULL_CHECKPOINT_UPLOAD
```
