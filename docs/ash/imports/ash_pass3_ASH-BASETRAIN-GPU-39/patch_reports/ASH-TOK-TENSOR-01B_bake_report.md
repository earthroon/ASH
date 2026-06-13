# ASH-TOK-TENSOR-01B Bake Report

## Patch

```txt
ASH-TOK-TENSOR-01B
Tokenizer Tensor Adapter Shape Smoke /
Feature Row To Hidden Residual Receipt /
No Model Forward No Weight Commit Seal
```

## Applied Files

```txt
crates/model_core/src/ash_tok_tensor_01b_tokenizer_tensor_adapter_shape_smoke.rs
crates/model_core/src/bin/ash_tok_tensor_01b_tokenizer_tensor_adapter_shape_smoke.rs
crates/model_core/src/lib.rs
crates/model_core/Cargo.toml
acceptance_reports/ASH-TOK-TENSOR-01B.md
patch_reports/ASH-TOK-TENSOR-01B_bake_report.md
ASH_TOK_TENSOR_01B_SHAPE_SMOKE_RECEIPT.json
ASH_TOK_TENSOR_01B_ADAPTER_SHAPE_CONTRACT.json
ASH_TOK_TENSOR_01B_STATIC_CHECKS.txt
ASH_TOK_TENSOR_01B_BAKE_MANIFEST.json
ASH_TOK_TENSOR_01B_LOCAL_VALIDATION.txt
```

## Closed Guards

```txt
side_channel_only_path_allowed=false
feature_attached_but_not_consumed=false
model_hidden_stream_unaware=false
vocab_expanded=false
token_id_remapped=false
embedding_row_reordered=false
full_safetensors_load_executed=false
row_parity_probe_executed=false
model_forward_executed=false
generation_forward_executed=false
optimizer_step_executed=false
weight_commit_executed=false
safetensors_mutation=false
```

## Validation Scope

Static file and receipt validation only. `cargo` and `rustc` are not available in this container, so compile validation is not run.
