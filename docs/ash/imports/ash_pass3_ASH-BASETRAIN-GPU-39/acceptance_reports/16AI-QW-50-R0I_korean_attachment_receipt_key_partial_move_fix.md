# QW-50-R0I — korean attachment receipt key partial move fix

## Scope

- Target crate: `ash_core`
- Target file: `crates/ash_core/src/word_context_korean_attachment.rs`

## Fix

- Replaced direct move of `first.deterministic_receipt_key` with `first.deterministic_receipt_key.clone()`.
- Also preserved `first.center_cue_id` with `first.center_cue_id.clone()` because `first` is borrowed later for attachment counting.
- Kept Korean attachment counting and receipt semantics unchanged.

## Static Pattern Check

- `first_receipt_key: first.deterministic_receipt_key.clone()` present.
- direct `first_receipt_key: first.deterministic_receipt_key,` removed.
- `center_cue_id: first.center_cue_id.clone()` present.
- direct `center_cue_id: first.center_cue_id,` removed.
- later `count_kind(&first, ...)` and `count_ending_like(&first)` borrow paths preserved.

## Guard

- No Korean attachment policy change.
- No count logic change.
- No receipt hash/key formula change.
- No runtime pointer mutation.
- No adapter registry mutation.
- No production apply.

## Verification

```txt
cargo check -p ash_core --lib
```

## Status

PENDING_LOCAL_CARGO_CHECK
