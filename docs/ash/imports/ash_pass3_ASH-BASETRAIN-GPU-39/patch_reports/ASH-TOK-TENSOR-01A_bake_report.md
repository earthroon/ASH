# ASH-TOK-TENSOR-01A Bake Report

## 확정

`ASH-TOK-TENSOR-01A` adds a receipt-only adapter binding contract that promotes QWave/Cheonjiin tokenizer-aligned tensor features into a hidden residual injection path.

The previous `ASH-TOK-TENSOR-01` incomplete safetensors sentinel is preserved. This patch does not rewrite its meaning.

## Added Files

```txt
crates/model_core/src/ash_tok_tensor_01a_tokenizer_tensor_adapter_binding.rs
crates/model_core/src/bin/ash_tok_tensor_01a_tokenizer_tensor_adapter_binding.rs
acceptance_reports/ASH-TOK-TENSOR-01A.md
patch_reports/ASH-TOK-TENSOR-01A_bake_report.md
ASH_TOK_TENSOR_01A_STATIC_CHECKS.txt
ASH_TOK_TENSOR_01A_ADAPTER_CONTRACT.json
ASH_TOK_TENSOR_01A_ADAPTER_RECEIPT.json
ASH_TOK_TENSOR_01A_BAKE_MANIFEST.json
```

## Modified Files

```txt
crates/model_core/src/lib.rs
crates/model_core/Cargo.toml
```

## Contract

```txt
token_ids[B,T] -> embedding_hidden[B,T,H]
tokenizer_tensor_features[B,T,F] -> feature_norm -> projection(F->H) and gate(F->H) -> output_norm -> residual_scale
final_hidden = embedding_hidden + adapter_hidden
```

## Closed Paths

```txt
vocab expansion
token id remap
embedding row reorder
reserved signal token as numeric feature carrier
side-channel-only metadata path
logits-only injection
decode text postprocess injection
safetensors full load
base model weight commit
optimizer step
row parity probe
```

## Validation

Static artifact validation and ZIP integrity were executed in the bake environment. `cargo`/`rustc` were not available, so compile validation is marked not run.
