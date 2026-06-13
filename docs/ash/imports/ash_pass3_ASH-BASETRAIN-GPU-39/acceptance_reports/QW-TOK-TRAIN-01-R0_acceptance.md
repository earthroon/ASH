# QW-TOK-TRAIN-01-R0 Acceptance

## Status

`PARTIAL_QW_TOK_TRAIN01_R0_BAKED_STATIC_PATCH_READY`

## Accepted static changes

- TRAIN-01 model spec parser now checks `[dimensions]` for `vocab_size` and `hidden_size`.
- TRAIN-01 failure output now renders a structured JSON summary instead of only `FAIL_QW_TOK_TRAIN01_PRECONDITION`.
- Report writing remains serde_json-based.
- No training, optimizer, gradient, GPU kernel, decode, checkpoint write, or tensor mutation was added.

## Local validation required

Run:

```powershell
cargo build -p model_core --bin qw_tok_train01_embedding_lmhead_atlas_adapt -j 1

.\target\debug\qw_tok_train01_embedding_lmhead_atlas_adapt.exe `
  --model-spec ".\specs\model_spec_v5_48259.toml" `
  --tokenizer ".\tokenizer_v5\artifacts\tokenizer_manifest_v5_final.json" `
  --checkpoint ".\tokenizer_v5\artifacts\full_model_vocab_v5_resized.train00_r2_metadata_rebound.safetensors" `
  --corpus ".\tokenizer_v5\corpus_v2\train\tokenizer_train_v5_dedup.txt" `
  --dry-run

Get-Content ".\artifacts\qw_tok_train01_embedding_lmhead_atlas_adaptation_report.json" -Raw |
  ConvertFrom-Json |
  Select-Object status
```

## PASS criteria

- `model_spec_ssot.vocab_size = 48259`
- `model_spec_ssot.hidden_size = 2048`
- `model_spec_ssot.failures = []`
- `tensor_key_probe.failures = []`
- `embedding_key = model.embed_tokens.weight`
- `lm_head_key = lm_head.weight`
- report passes `ConvertFrom-Json`
- no training/weight/checkpoint mutation occurs
