# Commit 16X Static Verify

## Verified in this bake

```text
python -m py_compile scripts/commit_16x_checkpoint_fingerprint.py scripts/commit_16x_verify_fingerprint.py
```

Result:

```text
[OK] python scripts compile
```

A synthetic safetensors header was generated in `/tmp/ash16x_test/fake.safetensors` and the sidecar generator produced:

```text
[16X] checkpoint_id=fake
[16X] tokenizer_vocab_size=48259
[16X] model_spec_vocab_size=56000
[16X] embedding_shape=[48259, 768]
[16X] lm_head_shape=[48259, 768]
[16X] status=retrofilled
[16X][WARN] model_spec_vocab_size differs from tokenizer_vocab_size
```

The verifier returned:

```json
{
  "fingerprint_valid": true,
  "checkpoint_hash_ok": true,
  "tokenizer_hash_ok": true,
  "model_spec_hash_ok": true,
  "dataset_hash_ok": null,
  "tensor_shape_ok": true,
  "warnings": [
    "model_spec_vocab_size differs from tokenizer_vocab_size"
  ]
}
```

## Not verified in this environment

```text
Rust cargo build / rustfmt
```

Reason:

```text
rustc/cargo is not installed in the execution environment.
```

## Important expected warning

The bundled tokenizer manifest has vocab size 48259, while `specs/model_spec.toml` declares 56000. 16X intentionally records this as a warning/mismatch reason instead of stopping inference.
