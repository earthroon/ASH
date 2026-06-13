# QW-TOK-TRAIN-01 Acceptance

## Status

`PARTIAL_QW_TOK_TRAIN01_BAKED_PROBE_PLAN_READY`

## Confirmed in bake

- Added `crates/model_core/src/tokenizer_v5_embedding_lmhead_atlas_adaptation.rs`.
- Added `crates/model_core/src/bin/qw_tok_train01_embedding_lmhead_atlas_adapt.rs`.
- Exported the module through `crates/model_core/src/lib.rs`.
- Added artifact paths for tensor key probe, LMHead atlas plan, repeat focus row probe, training receipt, no-transformer-update receipt, checkpoint write receipt, and smoke matrix.

## Safety contract

- No transformer block update.
- No attention/FFN/norm/rotary mutation.
- No original checkpoint overwrite.
- No tensor payload decode in the baked probe.
- `--train-lm-head-only` requests are converted into a PARTIAL plan until the actual WebGPU update kernel is sealed.

## Local validation command

```powershell
cargo build -p model_core --bin qw_tok_train01_embedding_lmhead_atlas_adapt -j 1

cargo run -p model_core --bin qw_tok_train01_embedding_lmhead_atlas_adapt -- `
  --model-spec ".\specs\model_spec_v5_48259.toml" `
  --tokenizer ".\tokenizer_v5\artifacts\tokenizer_manifest_v5_final.json" `
  --checkpoint ".\tokenizer_v5\artifacts\full_model_vocab_v5_resized.train00_r2_metadata_rebound.safetensors" `
  --corpus ".\tokenizer_v5\corpus_v2\train\tokenizer_train_v5_dedup.txt" `
  --dry-run
```
