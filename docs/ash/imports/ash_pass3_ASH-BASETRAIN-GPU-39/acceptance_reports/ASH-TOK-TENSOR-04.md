# ASH-TOK-TENSOR-04 Acceptance Report

## Verdict

```txt
PASS_ASH_TOK_TENSOR_04_BASETRAIN_ATLAS_ROUTE_CONFIG_REBIND_NO_INIT_CHECKPOINT_FULL_LOAD
```

## Seal

- base_train_route_config_added: true
- atlas_grouped_sequential_route_selectable: true
- tensor_group_manifest_cli_bound: true
- atlas_group_plan_cli_bound: true
- sequential_load_plan_cli_bound: true
- no_full_checkpoint_load_guard_added: true
- init_checkpoint_full_load_default: false
- load_full_checkpoint_weights_default_route: false
- load_full_checkpoint_into_model_full_upload_default: false

## Closed

- full_safetensors_load_executed: false
- full_checkpoint_upload_executed: false
- full_embedding_materialized: false
- full_lm_head_materialized: false
- row_parity_probe_executed: false
- model_forward_executed: false
- optimizer_step_executed: false
- weight_commit_executed: false
- safetensors_mutation: false

## Notes

ASH-TOK-TENSOR-04 changes base_train CLI/config/training route selection so init checkpoint paths no longer become the default monolithic checkpoint load route. Actual atlas group load remains deferred.
