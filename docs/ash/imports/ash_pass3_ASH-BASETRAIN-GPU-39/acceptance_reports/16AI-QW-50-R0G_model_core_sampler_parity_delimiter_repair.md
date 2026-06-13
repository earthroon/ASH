# QW-50-R0G — model_core sampler parity delimiter repair

## Scope

- Target crate: `model_core`
- Target file: `crates/model_core/src/sampler_parity.rs`

## Fix

- Repaired the unclosed delimiter in the `compare_traces(...) -> SamplerParityReceipt` function.
- Added the missing closing brace before `append_receipt(...)`.
- Normalized the multiline transition probe mutation `if / else if` braces around `selected_id_changed` conditions.
- Preserved sampler parity decision semantics and receipt structure.

## Guard

- No sampler parity score mutation.
- No selected-id drift condition removal.
- No receipt hash/key formula mutation.
- No runtime pointer mutation.
- No adapter registry mutation.
- No production apply.

## Verification

```txt
cargo check -p model_core --lib
```

## Status

PENDING_LOCAL_CARGO_CHECK
