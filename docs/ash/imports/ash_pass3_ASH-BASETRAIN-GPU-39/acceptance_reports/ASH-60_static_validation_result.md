# ASH-60 Static Validation Result

## Status
STATIC_VALIDATION_COMPLETED_WITHOUT_RUST_TOOLCHAIN

## Checked
- New module exists: crates/ash_core/src/runtime_lora_hot_reload_explicit_apply_candidate.rs
- New test exists: crates/ash_core/tests/ash_60_runtime_lora_hot_reload_explicit_apply_candidate.rs
- Acceptance report exists: acceptance_reports/ASH-60_runtime_lora_hot_reload_bridge_explicit_apply_candidate.md
- lib.rs contains `pub mod runtime_lora_hot_reload_explicit_apply_candidate;`
- lib.rs contains `pub use runtime_lora_hot_reload_explicit_apply_candidate::*;`
- Runtime attach / explicit apply commit / current pointer / receipt / registry mutation / artifact write / rollback snapshot flags are sealed false.
- The module creates an ASH-48-compatible envelope but does not call the ASH-48 apply gate.
- Deterministic candidate/envelope id tests are present.

## Not Run
- `cargo test -p ash_core ash_60 -- --nocapture`

## Reason
The execution container does not provide `cargo` or `rustc`.
