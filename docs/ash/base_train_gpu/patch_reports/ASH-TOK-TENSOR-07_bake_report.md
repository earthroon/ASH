# ASH-TOK-TENSOR-07 Bake Report

## Patch
BaseTrain Atlas Group Shadow Step / No Full Model Optimizer State Seal

## Base
ASH-TOK-TENSOR-06 baked tree.

## Files Patched
- crates/base_train/src/config.rs
- crates/base_train/src/training.rs
- crates/base_train/src/pipeline.rs
- crates/model_core/src/ash_tok_tensor_07_basetrain_atlas_group_shadow_step.rs
- crates/model_core/src/bin/ash_tok_tensor_07_basetrain_atlas_group_shadow_step.rs
- crates/model_core/src/lib.rs
- crates/model_core/Cargo.toml

## Artifacts
- ASH_TOK_TENSOR_07_SHADOW_STEP_RECEIPT.json
- ASH_TOK_TENSOR_07_SHADOW_DELTA_CONTRACT.json
- ASH_TOK_TENSOR_07_OPTIMIZER_SCOPE_CONTRACT.json
- ASH_TOK_TENSOR_07_STATIC_CHECKS.txt
- ASH_TOK_TENSOR_07_LOCAL_VALIDATION.txt
- ASH_TOK_TENSOR_07_BAKE_MANIFEST.json

## Verdict
```txt
PASS_ASH_TOK_TENSOR_07_BASETRAIN_ATLAS_GROUP_SHADOW_STEP_NO_FULL_MODEL_OPTIMIZER_STATE
```

## Notes
AtlasGroupedSequential route records shadow delta candidate receipts and does not create the legacy full HybridTrainModel optimizer state. Legacy optimizer fallback remains isolated behind blocked/non-default routes.
