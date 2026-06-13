# QW-TOK-TRAIN-00 Acceptance — Tokenizer V5 Checkpoint Rebind / No Training Seal

## Result

`PARTIAL_QW_TOK_TRAIN00_REBIND_METADATA_COMPARISON_PENDING`

## Confirmed

- `specs/model_spec_v5_48259.toml` identity was rebound from v4 residue to `model_tinyllama_1p1b_v5_48259`.
- `vocab_size = 48259` was preserved.
- tokenizer manifest top-level `manifest_hash` is not present in the baked manifest.
- `hashes.manifest_hash` exists.
- `tokenizer_v5/artifacts/tokenizer_manifest_v5_final.json` was materialized for runtime path parity.
- No training path was executed.
- No checkpoint file was modified.

## Pending On Operator Machine

The baked zip does not include `tokenizer_v5/artifacts/full_model_vocab_v5_resized.safetensors`, so checkpoint metadata hash comparison remains pending until the inspector is run in the local project directory.

## No Training Receipt

```json
{
  "training_executed": false,
  "forward_training_executed": false,
  "backward_executed": false,
  "gradient_created": false,
  "optimizer_created": false,
  "optimizer_step_executed": false,
  "weight_mutation_executed": false,
  "embedding_mutation_executed": false,
  "lm_head_mutation_executed": false,
  "transformer_block_mutation_executed": false,
  "decode_generation_executed": false,
  "checkpoint_write_executed": false
}
```

## Required Local Check

```powershell
cargo run -p model_core --bin qw_tok_train00_checkpoint_rebind_inspector -- `
  --model-spec ".\specs\model_spec_v5_48259.toml" `
  --tokenizer ".	okenizer_v5rtifacts	okenizer_manifest_v5_final.json" `
  --checkpoint ".	okenizer_v5rtifactsull_model_vocab_v5_resized.safetensors"
```
