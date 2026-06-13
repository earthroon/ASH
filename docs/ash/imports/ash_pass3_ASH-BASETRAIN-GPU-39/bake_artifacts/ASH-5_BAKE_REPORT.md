# ASH-5 Bake Report

## Commit
ASH-5 — Hard Negative Replay Buffer

## Status
Baked

## Files
- crates/ash_core/src/replay.rs
- crates/ash_core/src/bin/ash_replay_audit.rs
- crates/ash_core/tests/ash_5_hard_negative_replay.rs
- crates/ash_core/src/lib.rs
- acceptance_reports/ASH-5_hard_negative_replay_buffer.md

## Seal
Hard negative replay records are domain metadata only. ash_core does not write datasets, execute LoRA training, load safetensors, or run runtime forward.

## Validation
Rust-native only:

```powershell
cargo test -p ash_core ash_5_hard_negative_replay
cargo run -p ash_core --bin ash_replay_audit
```

No Python validator is present for ASH-5.
