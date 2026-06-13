# QW-50-R0N — Decode03C top-k usize/u32 alignment fix

## Scope

- Target crate: `model_core`
- Target file:
  - `crates/model_core/src/decode03c_shadow_policy.rs`

## Fix

- Aligned `current_top_k_from_entropy(...) -> usize` with `Decode03AEntropyStepReceipt.decode_config.top_k_effective` being stored as `u32`.
- Converted the receipt value to `usize` at the map boundary:
  - `r.decode_config.top_k_effective as usize`
- Preserved the existing environment fallback:
  - `env_usize("ASH_DECODE03C_CURRENT_TOP_K", 0)`

## Guard

- No Decode03C policy mutation.
- No top-k fallback mutation.
- No guard overlay mutation.
- No runtime pointer mutation.
- No adapter registry mutation.
- No production apply.
- No panic-based `try_into().unwrap()` conversion introduced.

## Verification

```txt
cargo check -p model_core --lib
```

## Status

PENDING_LOCAL_CARGO_CHECK
