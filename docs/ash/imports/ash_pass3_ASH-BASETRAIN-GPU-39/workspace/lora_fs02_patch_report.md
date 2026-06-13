# 16AI-QW-38G-R6A-LORA-FS-02

## Shared Hidden Token Head LoRA Trainer / Single Safetensors Export Seal

## Status

- status: `PASS_STATIC_LORA_FS02_TRAIN_EXPORT_BAKED_PENDING_LOCAL_CARGO_BUILD`
- cargo build in bake environment: `not available`
- command added: `lora.feature_store.train_export`

## Implemented

- Added `crates/orchestrator_local/src/lora_feature_store_train.rs`.
- Registered `lora.feature_store.train_export` in `orchestrator_local` command dispatch.
- Added shard-by-shard safetensors streaming reader.
- Added sampled-softmax style token trainer for `shared_hidden_token_head_lora`.
- Added dry-run and full export paths.
- Added manual safetensors writer for:
  - `adapter.shared_hidden_token_head.lora_A`
  - `adapter.shared_hidden_token_head.lora_B`
  - `adapter.shared_hidden_token_head.alpha`
- Added adapter manifest export.
- Added trainer receipt, export receipt, and JSONL loss ledger paths.
- Carried forward the SAMPLER-01A `min_p` initializer hotfix in `candidate_output.rs`.

## Safety

This patch creates a separate domain adapter artifact only. It does not mutate the base checkpoint, tokenizer, lm_head, final_norm, safetensors base file, or persistent ban mask.
