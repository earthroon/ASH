# QW-50-R0V — Hard Negative Replay Buffer SSOT Test Import Split Fix

## Scope

- `crates/ash_core/tests/ash_22_hard_negative_replay.rs`
- `crates/ash_core/tests/ash_27_hard_negative_replay_eval.rs`
- `crates/ash_core/tests/ash_22_synapse_suppression.rs`

## Fix

- Reverted ASH-22/27 hard-negative replay tests from `ash_core::replay::AshHardNegativeReplayBuffer` to `ash_core::hard_negative_replay::AshHardNegativeReplayBuffer`.
- Added the explicit hard-negative replay buffer import to tests that construct buffers with `cases`, `max_cases`, and `last_updated_unix_ms`.
- Preserved ASH-5 replay-buffer tests on `ash_core::replay::AshHardNegativeReplayBuffer`, because that type uses `version` and `records`.

## SSOT

- `ash_core::replay::AshHardNegativeReplayBuffer`: ASH-5 replay buffer surface with `version` and `records`.
- `ash_core::hard_negative_replay::AshHardNegativeReplayBuffer`: ASH-22/27 hard-negative replay surface with `version`, `cases`, `max_cases`, and `last_updated_unix_ms`.

## Guard

- No root compatibility alias added.
- No hard-negative case renamed to buffer.
- No test assertions removed.
- No production/runtime mutation.

## Verification

```txt
cargo check --workspace --all-targets
```

## Status

PENDING_LOCAL_CARGO_CHECK
