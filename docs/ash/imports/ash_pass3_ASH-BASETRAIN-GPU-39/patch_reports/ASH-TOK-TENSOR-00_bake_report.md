# ASH-TOK-TENSOR-00 Bake Report

## 반영 파일

```txt
crates/model_core/src/ash_tok_tensor_00_vocab_freeze_external_refs.rs
crates/model_core/src/bin/ash_tok_tensor_00_vocab_freeze_external_refs.rs
crates/model_core/src/lib.rs
acceptance_reports/ASH-TOK-TENSOR-00.md
patch_reports/ASH-TOK-TENSOR-00_bake_report.md
ASH_TOK_TENSOR_00_STATIC_CHECKS.txt
ASH_TOK_TENSOR_00_BAKE_MANIFEST.json
```

## Asset vendoring guard

The bake output intentionally excludes:

```txt
tokenizer_manifest_v5_final.json
tokenizer_manifest_v5_final.before_manifest_hash_cleanup.json
tokenizer_v5.vocab
tokenizer_v5.model
ash_v5_native_genesis.forge01_smoke.safetensors
```

These assets are external references only.

## 다음 패치

```txt
ASH-TOK-TENSOR-01
Safetensors Embedding Row Parity Probe /
No Weight Mutation No Model Forward Seal
```
