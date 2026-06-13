# ASH-TOK-TENSOR-09 Bake Report

## Title

Grouped Embedding LMHead Row Parity Probe / Header-Resolved Key Only No Full Tensor Load Seal

## Implemented files

- crates/model_core/src/ash_tok_tensor_09_grouped_embedding_lmhead_row_parity_probe.rs
- crates/model_core/src/bin/ash_tok_tensor_09_grouped_embedding_lmhead_row_parity_probe.rs
- crates/model_core/src/lib.rs
- crates/model_core/Cargo.toml
- ASH_TOK_TENSOR_09_ROW_PARITY_PROBE_RECEIPT.json
- ASH_TOK_TENSOR_09_EMBEDDING_ROW_PARITY_REPORT.json
- ASH_TOK_TENSOR_09_LMHEAD_ROW_PARITY_REPORT.json
- ASH_TOK_TENSOR_09_AXIS_RESOLUTION_REPORT.json
- ASH_TOK_TENSOR_09_STATIC_CHECKS.txt

## Boundary

This bake creates a header-resolved vocab-axis parity probe contract. It intentionally does not package tokenizer/model/safetensors source assets and does not perform payload decode.

## Verdict

```txt
PASS_ASH_TOK_TENSOR_09_GROUPED_EMBEDDING_LMHEAD_ROW_PARITY_PROBE_HEADER_RESOLVED_KEY_ONLY_NO_FULL_TENSOR_LOAD
```
