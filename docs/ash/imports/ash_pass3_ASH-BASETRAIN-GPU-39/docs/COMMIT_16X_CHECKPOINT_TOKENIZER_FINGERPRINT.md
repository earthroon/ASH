# Commit 16X — Checkpoint Tokenizer Fingerprint Seal

## SSOT

Checkpoint provenance is now sealed as a first-class runtime probe.

```text
checkpoint metadata / sidecar
→ tokenizer manifest hash + vocab
→ model spec hash + declared vocab
→ checkpoint embedding/lm_head shape
→ runtime output artifact checkpoint_fingerprint block
```

16X does **not** hard-fail inference. That enforcement belongs to 16Y.

## Added files

```text
crates/runtime/src/checkpoint_fingerprint.rs
scripts/commit_16x_checkpoint_fingerprint.py
scripts/commit_16x_verify_fingerprint.py
artifacts/checkpoint_meta/.gitkeep
```

## Changed files

```text
crates/runtime/Cargo.toml
crates/runtime/src/lib.rs
crates/runtime/src/infer.rs
crates/orchestrator_local/src/infer_entry.rs
docs/COMMIT_16X_CHECKPOINT_TOKENIZER_FINGERPRINT.md
```

## Runtime behavior

Every standard inference result now carries:

```json
{
  "checkpointFingerprint": {
    "schema_version": "ash.checkpoint_fingerprint.runtime_probe.v1",
    "status": "missing|retrofilled|partial|invalid|sealed",
    "fingerprint_source": "embedded_safetensors_metadata|sidecar_json|missing",
    "provenance_missing": true,
    "fingerprint_sidecar_path": null,
    "checkpoint_id": null,
    "runtime_tokenizer_manifest_sha256": "sha256:...",
    "runtime_tokenizer_vocab_size": 48259,
    "checkpoint_tokenizer_hash": null,
    "checkpoint_tokenizer_hash_matches_runtime": null,
    "runtime_model_spec_vocab_size": 56000,
    "checkpoint_embedding_vocab_size": null,
    "checkpoint_lm_head_vocab_size": null,
    "warnings": ["checkpoint_fingerprint_sidecar_missing"],
    "mismatch_reasons": ["runtime_model_spec_vocab_mismatch"]
  }
}
```

The artifact JSON also includes snake_case aliases:

```text
checkpoint_fingerprint
checkpoint_fingerprint_probe
```

The immediate response JSON includes camelCase aliases:

```text
checkpointFingerprint
checkpointFingerprintProbe
```

## Sidecar discovery order

For the first checkpoint path, runtime checks:

```text
1. embedded safetensors __metadata__["ash.checkpoint_fingerprint"]
2. <checkpoint_stem>.fingerprint.json
3. <checkpoint_file_name>.fingerprint.json
4. artifacts/checkpoint_meta/<checkpoint_stem>.fingerprint.json
```

If no sidecar exists, inference continues and the probe reports:

```text
status = missing
provenance_missing = true
```

## Sidecar generation

```bash
python scripts/commit_16x_checkpoint_fingerprint.py \
  --checkpoint checkpoints/ash_base.safetensors \
  --tokenizer-manifest artifacts/tokenizer_manifest_v5_final.json \
  --model-spec specs/model_spec.toml \
  --dataset-manifest manifests/v4_guarded_dataset_manifest.json \
  --checkpoint-id ash_base_pass3 \
  --out artifacts/checkpoint_meta/ash_base_pass3.fingerprint.json
```

If tensor names differ, override them:

```bash
python scripts/commit_16x_checkpoint_fingerprint.py \
  --checkpoint checkpoints/ash_base.safetensors \
  --tokenizer-manifest artifacts/tokenizer_manifest_v5_final.json \
  --model-spec specs/model_spec.toml \
  --embedding-name model.embed_tokens.weight \
  --lm-head-name lm_head.weight
```

For old checkpoints where tensor names are unknown, emit a partial fingerprint:

```bash
python scripts/commit_16x_checkpoint_fingerprint.py \
  --checkpoint checkpoints/ash_base.safetensors \
  --tokenizer-manifest artifacts/tokenizer_manifest_v5_final.json \
  --model-spec specs/model_spec.toml \
  --allow-missing-tensors
```

## Verification

```bash
python scripts/commit_16x_verify_fingerprint.py \
  --fingerprint artifacts/checkpoint_meta/ash_base_pass3.fingerprint.json
```

The verifier checks:

```text
checkpoint_sha256
tokenizer_manifest_sha256
model_spec_sha256
dataset_manifest_sha256, if present
embedding/lm_head/bias tensor shapes, if present
```

## 16Y handoff values

The runtime probe now exposes these values for Commit 16Y hard gate:

```text
runtime_tokenizer_manifest_sha256
runtime_tokenizer_vocab_size
checkpoint_tokenizer_hash
checkpoint_tokenizer_vocab_size
runtime_model_spec_sha256
runtime_model_spec_vocab_size
checkpoint_model_spec_hash
checkpoint_model_spec_vocab_size
checkpoint_embedding_vocab_size
checkpoint_lm_head_vocab_size
special_token_ids
provenance_missing
warnings
mismatch_reasons
```

## Acceptance status

```text
AC-1 fingerprint sidecar JSON generation: implemented
AC-2 tokenizer manifest sha256 record: implemented
AC-3 tokenizer vocab_size record: implemented
AC-4 model_spec sha256 and declared vocab: implemented
AC-5 checkpoint embedding/lm_head shape record: implemented via safetensors header parser
AC-6 missing metadata reports provenance_missing: implemented
AC-7 runtime output artifact checkpoint_fingerprint block: implemented
AC-8 no hard fail in 16X: implemented
AC-9 16Y mismatch reason list: implemented
```
