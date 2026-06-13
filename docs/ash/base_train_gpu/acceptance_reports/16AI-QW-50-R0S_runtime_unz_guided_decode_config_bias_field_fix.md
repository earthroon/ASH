# QW-50-R0S — runtime_unz GuidedDecodeConfig Bias Field Fix

## Scope

- Target crate: `runtime_unz_legacy`
- Target file:
  - `crates/runtime_unz/src/infer.rs`

## Fix

- Added missing `glossary_hit_bias` and `tm_hit_bias` fields to the `GuidedDecodeConfig` base initializer.
- Kept translation task profile overrides intact.
- Kept non-translation default bias neutral at `0.0`.

## Guard

- No decode policy mutation beyond completing required struct initialization.
- No model/runtime pointer mutation.
- No adapter registry mutation.
- No production apply.

## Verification

```txt
cargo check --workspace --all-targets
```

## Status

PENDING_LOCAL_CARGO_CHECK
