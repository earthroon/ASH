# QW-50-R0F — receipt hash borrow/move scope fix

## Scope

- Target crate: `ash_core`
- Target files:
  - `crates/ash_core/src/transition_guard_receipt.rs`
  - `crates/ash_core/src/korean_morph_salad_receipt.rs`
  - `crates/ash_core/src/candidate_recovery_receipt.rs`

## Fix

- Moved `ReceiptKeyMaterial` construction into a local block.
- Computed `deterministic_receipt_key` before moving owned hash `String` values into receipt structs.
- Replaced inline `decode04_q4_hash_json(&key_material)` field initializers with precomputed `deterministic_receipt_key`.
- Preserved receipt key inputs and hash formula semantics.

## Guard

- No guard policy mutation.
- No candidate recovery decision mutation.
- No morph salad score mutation.
- No runtime pointer mutation.
- No adapter registry mutation.
- No production apply.
- No silent unserializable fallback added.

## Static Pattern Check

See `artifacts/compile_recovery/qw50_r0f_static_pattern_check.json`.

## Verification

```txt
cargo check -p ash_core --lib
```

## Status

PENDING_LOCAL_CARGO_CHECK
