# QW-50-R0T — ash_core hard negative replay buffer import path fix

## Scope

- Target crate: `ash_core`
- Target file:
  - `crates/ash_core/tests/ash_5_hard_negative_replay.rs`

## Fix

- Imported `AshHardNegativeReplayBuffer` from `ash_core::replay` explicitly.
- Replaced stale root-path construction `ash_core::AshHardNegativeReplayBuffer { ... }` with direct `AshHardNegativeReplayBuffer { ... }`.
- Preserved duplicate fingerprint validation test semantics.
- Did not add a compatibility alias to the crate root.

## Guard

- No replay validation policy change.
- No duplicate fingerprint rule change.
- No hard negative replay case schema change.
- No runtime pointer mutation.
- No adapter registry mutation.
- No production apply.

## Static Pattern Check

See `artifacts/compile_recovery/qw50_r0t_static_pattern_check.json`.

## Verification

```txt
cargo check --workspace --all-targets
```

## Status

PENDING_LOCAL_CARGO_CHECK
