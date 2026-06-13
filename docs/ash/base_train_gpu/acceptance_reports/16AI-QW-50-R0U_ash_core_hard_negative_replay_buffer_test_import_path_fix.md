# QW-50-R0U — ash_core Hard Negative Replay Buffer Test Import Path Fix

## Scope

- Target crate: `ash_core`
- Target file:
  - `crates/ash_core/tests/ash_22_hard_negative_replay.rs`

## Fix

- Added explicit import for `AshHardNegativeReplayBuffer` from `ash_core::replay`.
- Preserved existing `AshHardNegativeReplayBuffer::default()` and struct literal test usage.
- Did not replace the buffer with `AshHardNegativeReplayCase`.
- Did not add a root-level compatibility alias.

## Guard

- No hard-negative replay policy change.
- No replay buffer validation logic change.
- No fixture semantics change.
- No runtime pointer mutation.
- No adapter registry mutation.
- No production apply.

## Static Pattern Check

See `artifacts/compile_recovery/qw50_r0u_static_pattern_check.json`.

## Verification

```txt
cargo check --workspace --all-targets
```

## Status

PENDING_LOCAL_CARGO_CHECK
