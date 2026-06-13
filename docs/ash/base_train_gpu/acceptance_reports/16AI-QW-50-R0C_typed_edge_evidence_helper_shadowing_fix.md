# QW-50-R0C — typed edge evidence helper shadowing fix

## Scope

- Target crate: `ash_core`
- Target file: `crates/ash_core/src/word_context_edge_registry.rs`

## Fix

- Renamed the typed edge evidence helper function from `evidence(...)` to `build_evidence(...)`.
- Replaced `evidence.push(evidence(...))` call sites with `evidence.push(build_evidence(...))`.
- Preserved the `evidence` Vec variable name to minimize unrelated churn.
- Cloned `first.deterministic_receipt_key` and `second.deterministic_receipt_key` when copying them into the case result, preventing partial move / later borrow failures.

## Static Verification

- `evidence.push(evidence(` pattern removed from `word_context_edge_registry.rs`.
- `fn evidence(` helper removed from `word_context_edge_registry.rs`.
- `fn build_evidence(` helper exists.
- Direct receipt-key moves in `first_receipt_key` / `second_receipt_key` assignments were replaced with `.clone()`.

## Guard

- No relation scoring policy change.
- No confidence band change.
- No evidence ordering change.
- No runtime pointer mutation.
- No adapter registry mutation.
- No production apply.

## Verification

```txt
cargo check -p ash_core --lib
```

## Status

PENDING_LOCAL_CARGO_CHECK

`cargo` / `rustc` were not available in this container, so native cargo validation must be run locally.
