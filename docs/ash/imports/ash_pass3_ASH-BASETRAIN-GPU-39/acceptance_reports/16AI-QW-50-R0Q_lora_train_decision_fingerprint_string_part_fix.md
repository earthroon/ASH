# QW-50-R0Q — lora_train Decision Fingerprint String Part Fix

## Scope

- `crates/lora_train/src/qwave_auxiliary_loss_candidate.rs`
- `crates/lora_train/src/hangul_structure_reconstruction_head.rs`
- `crates/lora_train/src/word_salad_negative_corpus.rs`

## Fix

- Converted decision enum values into stable string fingerprint parts by hashing the serializable decision enum first.
- Replaced direct `receipt.decision.clone()` entries in `short_sha256_parts(&[String])` arrays with `decision_hash`.
- Preserved the R0P tuple-splitting approach and avoided restoring long tuple fingerprints.

## Guard

- No candidate decision policy mutation.
- No loss/corpus guard mutation.
- No runtime pointer mutation.
- No adapter registry mutation.
- No production apply.

## Verification

```txt
cargo check --workspace --all-targets
```

## Status

PENDING_LOCAL_CARGO_CHECK
