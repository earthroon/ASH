# 16AI-6V-3-R1 Facade Runtime Output Writer Fix

## Purpose

Fix `af16ai6v3_tokenizer_v6_facade_probe` so that runtime PASS state is written to `--out-json`, `--out-md`, and `--out-acceptance` instead of leaving a bake placeholder as the source-gate SSOT.

## Scope

This patch does not change the facade decision logic, tokenizer modes, generation path, GPU path, vocab, token IDs, checkpoint, or embedding shape.

## Runtime SSOT Contract

When the console seal is `PASS_TOKENIZER_V6_FACADE`, the runtime output JSON must include:

```json
{
  "run": {
    "kind": "tokenizer_v6_facade_probe",
    "writer_fix": "16AI-6V-3-R1",
    "acceptance_status": "PASS_TOKENIZER_V6_FACADE"
  },
  "summary": {
    "acceptance_status": "PASS_TOKENIZER_V6_FACADE"
  }
}
```

## Failure Guard

A runtime result must not remain as `tokenizer_v6_facade_probe_bake_manifest` or `PENDING_RUNTIME` after successful execution.
