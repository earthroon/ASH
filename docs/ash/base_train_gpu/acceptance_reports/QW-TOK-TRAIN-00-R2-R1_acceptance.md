# QW-TOK-TRAIN-00-R2-R1 Acceptance

## Status

PATCHED_FOR_STACK_SAFE_DRY_RUN

## Acceptance criteria

- [x] `sha256_reader()` no longer allocates a 1 MiB array on the stack.
- [x] Streaming hash remains streaming and does not decode tensor payloads.
- [x] No weight tensor mutation path was added.
- [x] No training path was added.
- [x] No in-place checkpoint overwrite path was added.
- [x] Existing R2 approval gate remains intact.

## Local validation command

```powershell
cargo build -p model_core --bin qw_tok_train00_r2_metadata_rebind_commit -j 1

cargo run -p model_core --bin qw_tok_train00_r2_metadata_rebind_commit -- `
  --model-spec ".\specs\model_spec_v5_48259.toml" `
  --tokenizer ".\tokenizer_v5\artifacts\tokenizer_manifest_v5_final.json" `
  --checkpoint ".\tokenizer_v5\artifacts\full_model_vocab_v5_resized.safetensors"
```

Expected dry-run status:

```txt
PARTIAL_QW_TOK_TRAIN00_R2_OPERATOR_APPROVAL_REQUIRED_NO_WRITE
```

If model spec/tokenizer/checkpoint SSOT still has validation failures, status may be FAIL, but it should not stack overflow.
