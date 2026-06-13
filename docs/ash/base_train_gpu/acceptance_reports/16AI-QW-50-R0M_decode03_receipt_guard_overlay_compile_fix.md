# QW-50-R0M — Decode03 Receipt Field Depth / Guard Overlay Numeric Tuple Fix

## Scope

Target crate: `model_core`

Modified files:

- `crates/model_core/src/decode03c_shadow_policy.rs`
- `crates/model_core/src/salad02_detector.rs`
- `crates/model_core/src/salad04_korean_morph_guard.rs`
- `crates/model_core/src/decode03e_guard_overlay.rs`

## Fix

- Repointed `Decode03AEntropyStepReceipt` field access through `decode_config`:
  - `temperature` -> `decode_config.temperature`
  - `top_p` -> `decode_config.top_p`
  - `top_k_effective` -> `decode_config.top_k_effective`
  - `min_p` -> `decode_config.min_p`
- Removed direct reads of non-existent upstream status fields from `Decode03DStepReceipt` in Salad02 conversion.
- Added explicit `f32` typing for morph guard numeric max/clamp paths.
- Added explicit `f32` policy tuple annotation and literal suffixes in Decode03E guard overlay.
- Fixed `base_policy` else branch to return the required 7-element tuple including `reasons`.

## Guard

- No sampler policy mutation.
- No decode guard policy mutation.
- No runtime pointer mutation.
- No adapter registry mutation.
- No production apply.
- No silent fallback hash added.

## Verification

```txt
cargo check -p model_core --lib
```

## Status

PENDING_LOCAL_CARGO_CHECK
