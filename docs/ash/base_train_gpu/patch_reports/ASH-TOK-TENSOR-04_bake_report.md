# ASH-TOK-TENSOR-04 Bake Report

## Patch

```txt
ASH-TOK-TENSOR-04
BaseTrain Atlas Route Config Rebind /
No Init Checkpoint Full Load Seal
```

## Changed Runtime Files

```txt
crates/base_train/src/config.rs
crates/base_train/src/bin/base_train.rs
crates/base_train/src/lib.rs
crates/base_train/src/pipeline.rs
crates/base_train/src/training.rs
```

## Added Receipt/Contract Files

```txt
crates/model_core/src/ash_tok_tensor_04_basetrain_atlas_route_config_rebind.rs
crates/model_core/src/bin/ash_tok_tensor_04_basetrain_atlas_route_config_rebind.rs
ASH_TOK_TENSOR_04_ROUTE_REBIND_RECEIPT.json
ASH_TOK_TENSOR_04_ROUTE_CONFIG_CONTRACT.json
ASH_TOK_TENSOR_04_STATIC_CHECKS.txt
ASH_TOK_TENSOR_04_LOCAL_VALIDATION.txt
```

## Verdict

```txt
PASS_ASH_TOK_TENSOR_04_BASETRAIN_ATLAS_ROUTE_CONFIG_REBIND_NO_INIT_CHECKPOINT_FULL_LOAD
```

## Validation Boundary

Static validation only. cargo/rustc were not available in this container.
