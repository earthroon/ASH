# ASH-TOK-TENSOR-06 Bake Report

## Scope

Baked embedding/lm_head atlas shard contract on top of ASH-TOK-TENSOR-05.

## Added Files

```txt
crates/model_core/src/ash_tok_tensor_06_embedding_lmhead_atlas_shard_contract.rs
crates/model_core/src/bin/ash_tok_tensor_06_embedding_lmhead_atlas_shard_contract.rs
ASH_TOK_TENSOR_06_EMBEDDING_SHARD_CONTRACT.json
ASH_TOK_TENSOR_06_LMHEAD_SHARD_CONTRACT.json
ASH_TOK_TENSOR_06_ATLAS_SHARD_AXIS_CONTRACT.json
ASH_TOK_TENSOR_06_SHARD_RECEIPT.json
ASH_TOK_TENSOR_06_STATIC_CHECKS.txt
```

## Modified Files

```txt
crates/model_core/src/lib.rs
crates/model_core/Cargo.toml
```

## SSOT

Embedding and lm_head are contracted as atlas shards, not full materialized matrices. LMHead axis orientation remains deferred to grouped probe.

## Not Run

```txt
cargo validation = not_run_cargo_not_installed
rustc validation = not_run_rustc_not_installed
```
