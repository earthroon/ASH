# 16AI-QW-38G-R6A-SALAD-01B Static Validation

## Status

PASS_STATIC_SCOPE_HOTFIX_PENDING_LOCAL_CARGO_BUILD

## Confirmed

- Removed invalid `gate.audit` access from `crates/runtime/src/engine/generation_runner.rs`.
- `decode_profile` is captured while `gate` is still in scope.
- `word_salad_guard` is captured while `gate` is still in scope.
- Event payload still exposes SALAD-01 decode metadata.

## Pending

- Local `cargo build` / `cargo check`, because cargo is unavailable in the bake container.
