# QW-TOK-TRAIN-00-R1 Acceptance

## Status
`PARTIAL_QW_TOK_TRAIN00_R1_AUDIT_PENDING_CHECKPOINT_OR_HASH_KEYS`

## Confirmed
- Model spec V5 identity is inspected.
- Runtime tokenizer `hashes.manifest_hash` is inspected.
- Safetensors header audit code is added.
- Tensor payload loading is explicitly forbidden.
- Training, optimizer, decode, checkpoint rewrite, and metadata commit are not executed.

## Local pending condition
The baked archive does not include the heavy `tokenizer_v5/artifacts/full_model_vocab_v5_resized.safetensors` payload, so full checkpoint metadata comparison may remain PARTIAL until run in the local project workspace.

## Run
```powershell
cargo run -p model_core --bin qw_tok_train00_r1_safetensors_metadata_audit -- `
  --model-spec ".\specs\model_spec_v5_48259.toml" `
  --tokenizer ".\tokenizer_v5\artifacts\tokenizer_manifest_v5_final.json" `
  --checkpoint ".\tokenizer_v5\artifacts\full_model_vocab_v5_resized.safetensors" `
  --out ".\artifacts\qw_tok_train00_r1_safetensors_metadata_audit_report.json"
```
