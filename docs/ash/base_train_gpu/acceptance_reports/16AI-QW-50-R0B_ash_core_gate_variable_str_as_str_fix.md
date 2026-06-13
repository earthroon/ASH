# QW-50-R0B — ash_core gate variable / str_as_str fix

## Scope

- Target crate: `ash_core`
- Target files:
  - `crates/ash_core/src/word_context_mock_candidate_approval_fixture.rs`
  - `crates/ash_core/src/word_context.rs`

## Fix

- Connected `target_update_candidate_gate_open` to the existing `target_update_gate_open` value inside `build_approval_fixture_risk`.
- Removed unstable `.as_str()` call on an already borrowed string slice in `word_context.rs` by matching directly on `lower`.

## Guard

- No runtime pointer mutation.
- No target update execution change.
- No approval or production apply behavior change.
- No unrelated crate modification.

## Verification

```txt
cargo check -p ash_core --lib
```

## Static Verification Performed

```txt
- `target_update_candidate_gate_open` is now bound before struct literal use.
- `lower.as_str()` no longer appears in `crates/ash_core/src/word_context.rs`.
```

## Status

PENDING_LOCAL_CARGO_CHECK
